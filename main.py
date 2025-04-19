from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile, os, traceback, base64
from pydub import AudioSegment
from io import BytesIO
import asyncio
import edge_tts
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/api/generate", methods=["POST"])
def generate_audio():
    data = request.get_json()
    script = data.get("script", "")
    mode = data.get("mode", "script")
    voice_male = data.get("maleVoice", "en-US-GuyNeural")
    voice_female = data.get("femaleVoice", "en-US-JennyNeural")

    if not script:
        return jsonify({"error": "No script provided"}), 400

    if mode == "prompt":
        prompt = f"""
You are an English tutor helping a student practice IELTS Listening Part 1.

Generate a short, friendly and realistic conversation between two people (10–13 lines), in the style of IELTS Listening Part 1.

---

🎯 GOAL:
Make the conversation sound like real-life speech between two people.
It must include **at least 3 natural twists** from different categories.

---

🌀 You MUST include at least **three** of the following twist types, distributed naturally:

– Small correction:  
  “Actually, just two nights.”  
  “No wait, make that Saturday.”

– Hesitation or filler:  
  “Hmm… I think it’s the 20th.”  
  “Let me see... probably at two p.m.”

– Indecisiveness / Change of mind:  
  “Maybe a double? No, a single.”  
  “I thought Tuesday, but Friday works better.”

– Clarification / Check:  
  “Do you mean like my reference number?”  
  “You want me to spell that?”

❗ You must not reuse the same twist twice. Use different types.

---

🔡 SPELLING:
- Must break into a separate turn and include a **short pause before spelling**

📛 Names:
- Choose realistic, multicultural names.

🔢 FORMATTING:
- Phone: "Zero - Nine - Eight - One"
- Email: "a - b - c at gmail dot com"
- Times: "around five thirty"
- Money: "twelve pounds fifty"

---

Topic: {script}

Return only the conversation. One line per turn. No labels.
"""
        try:
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.9,
                messages=[{"role": "user", "content": prompt}]
            )
            script = res.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"error": f"Failed to generate dialogue from prompt: {str(e)}"}), 500

    lines = [line.strip() for line in script.strip().split("\n") if line.strip()]
    CHUNK_SIZE = 10
    chunks = [lines[i:i + CHUNK_SIZE] for i in range(0, len(lines), CHUNK_SIZE)]

    audio_chunks = []
    script_chunks = []

    async def synthesize_text(text, voice, out_path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        for chunk_index, chunk_lines in enumerate(chunks):
            tasks = []
            filenames = []
            script_chunks.append(chunk_lines)

            for idx, text in enumerate(chunk_lines):
                voice = voice_male if idx % 2 == 0 else voice_female
                filename = os.path.join(tmpdir, f"chunk{chunk_index}_line{idx}.mp3")
                filenames.append(filename)
                tasks.append(synthesize_text(text, voice, filename))

            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(asyncio.gather(*tasks))
            except Exception as e:
                return jsonify({"error": f"Audio generation error: {str(e)}"}), 500

            final_audio = AudioSegment.empty()
            for filename in filenames:
                seg = AudioSegment.from_file(filename)
                final_audio += seg + AudioSegment.silent(duration=200)

            buffer = BytesIO()
            final_audio.export(buffer, format="mp3", bitrate="64k")
            buffer.seek(0)
            audio_base64 = base64.b64encode(buffer.read()).decode("utf-8")
            audio_chunks.append(audio_base64)

    return jsonify({
        "audios": audio_chunks,
        "scripts": script_chunks
    })

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")  # Hoặc origin cụ thể
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response

@app.route("/api/generate-table", methods=["POST"])
def generate_ielts_table():
    data = request.get_json()
    script = data.get("script", "")
    if not script:
        return jsonify({"error": "Missing script"}), 400

    try:
        prompt = f"""
You are an IELTS Listening question generator.

Based on the conversation below, generate a **Table Completion** task for IELTS Listening Part 1.

✅ First, write a suitable instruction line (e.g. NO MORE THAN TWO WORDS AND/OR A NUMBER).
✅ Then generate a table in **markdown format** with exactly two columns:
   - Column 1: Field label (e.g. Name, Number of nights, Room type, Guest name, Booking date…)
   - Column 2: The correct answer (copied exactly from the conversation)

🧠 RULES:
– Return **at least 3 rows**, if available.
– Field labels must be **clear and specific**, avoid vague labels like “Type” or “Number”.
– The table rows must follow the **same order** as the details appear in the dialogue (top to bottom).
– DO NOT combine or summarize information from different lines.
– DO NOT make up new information. Use only what is **explicitly stated** in the conversation.
– DO NOT leave blanks — every answer cell must be filled.

✅ Format reminder: The table should have headers and rows like:

| Field label | Correct answer |
|-------------|----------------|
| (your data) | (from dialogue) |
---

Conversation:
{script}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        markdown_table = response.choices[0].message.content
        html = convert_markdown_table_to_tooltip_html(markdown_table)
        return jsonify({"html": html})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False, host='0.0.0.0', port=5000)
