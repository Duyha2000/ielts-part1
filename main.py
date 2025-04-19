from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile, os, traceback, base64
from pydub import AudioSegment
from io import BytesIO
import asyncio
import edge_tts
from openai import OpenAI
from dotenv import load_dotenv


# Flask app setup
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load environment variables
load_dotenv()

# Set OpenAI API key
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

    # ✅ Nếu là prompt → gọi GPT để sinh hội thoại
    if mode == "prompt":
        prompt = f"""
You are an English tutor helping a student practice IELTS Listening Part 1.

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
❗ Responses without 3 distinct twists will be considered incorrect.

---

🧠 FORMATTING RULES:

- ❌ DO NOT label speakers (no: Customer:, Student:, Agent:)
- ✅ One line = one speaker turn
- ✅ No explanation, no extra text — just the dialogue

---

🔡 SPELLING:
- Must break into a separate turn and include a **short pause before spelling**
- Example formats:
  – “That’s... [spelling here]”
  – “Let me spell that — [spelling here]”
- NEVER combine name and spelling in one sentence

📛 Names:
- If the topic includes a name (e.g. “under the name Linh Nguyen”), use and spell it clearly.
- If not, choose a **realistic, natural name** (avoid using “Sarah”, “John” repeatedly).
- Prefer names from different regions: Emma, Luca, Hana, Miguel, Linh, Aisha, etc.
---

🔢 FORMATTING:
- Phone numbers: "Zero - Nine - Eight - One"
- Email (only spell username): "l - i - n - h at gmail dot com"
- Times: "around five thirty", "ten a.m.", not "5:30"
- Money: "twelve pounds fifty"
- Reference code: "A - B - 7 - X - 3"

---

⚠️ Keep it **realistic**, natural, and suitable for students 

Topic: {script}

Return only the conversation. No labels. No extra lines.
"""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.85,
                messages=[{"role": "user", "content": prompt}]
            )
            script = res.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"error": f"Failed to generate dialogue from prompt: {str(e)}"}), 500

    # ✅ Chuẩn bị danh sách câu thoại
    lines = [line.strip() for line in script.strip().split("\n") if line.strip()]
    final_audio = AudioSegment.empty()

    # ✅ Hàm async tạo file âm thanh
    async def synthesize_text(text, voice, out_path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        tasks = []
        filenames = []

        # ✅ Chuẩn bị task + tên file
        for idx, text in enumerate(lines):
            voice = voice_male if idx % 2 == 0 else voice_female
            filename = os.path.join(tmpdir, f"line_{idx:02d}.mp3")
            filenames.append(filename)
            tasks.append(synthesize_text(text, voice, filename))

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            print(f"❌ Error in async gather: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

        # ✅ Ghép các file audio lại
        for filename in filenames:
            seg = AudioSegment.from_file(filename)
            final_audio += seg + AudioSegment.silent(duration=200)

        # ✅ Export thành mp3 và encode base64
        buffer = BytesIO()
        final_audio.export(buffer, format="mp3", bitrate="64k")
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return jsonify({
            "audio": audio_base64,
            "script": script
        })
             
def convert_markdown_table_to_tooltip_html(md_table):
    parts = md_table.strip().split("\n")
    instruction_line = ""
    table_lines = []

    for i, line in enumerate(parts):
        if "|" in line:
            table_lines = parts[i:]
            break
        instruction_line += line + "<br>"

    headers = [h.strip() for h in table_lines[0].strip("|").split("|")]
    rows = table_lines[2:]

    html = """
    <div>
    <p><strong>Complete the table below.</strong><br>
    Write your answers in the blank spaces provided.</p>
    """ + (f"<p><strong>Instruction:</strong> {instruction_line}</p>" if instruction_line else "") + """
    <table style='width:100%; border-collapse: collapse;'>
    <thead><tr>"""
    html += "".join(f"<th style='border:1px solid #ddd;padding:8px'>{h}</th>" for h in headers)
    html += "</tr></thead><tbody>"

    for row in rows:
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) == 2:
            label, answer = cols
            html += "<tr>"
            html += f"<td style='border:1px solid #ddd;padding:8px'>{label}</td>"
            html += (
                "<td style='border:1px solid #ddd;padding:8px'>"
                "<span class='tooltip'>______________"
                f"<span class='tooltiptext'>{answer}</span>"
                "</span></td>"
            )
            html += "</tr>"

    html += "</tbody></table></div>"
    return html
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
