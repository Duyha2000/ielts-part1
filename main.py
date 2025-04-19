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

Given the topic below, write a short natural conversation (about 10 lines), like in the IELTS Listening exam.

Make it realistic and friendly, and DO NOT label speakers (no "Speaker 1:", "Speaker A:", or names).

Prompt: {script}

Just write the dialogue, one line per speaker.
"""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.6,
                messages=[{"role": "user", "content": prompt}]
            )
            script = res.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"error": f"Failed to generate dialogue from prompt: {str(e)}"}), 500

    # ✅ Tạo audio từ đoạn hội thoại
    lines = [line.strip() for line in script.strip().split("\n") if line.strip()]
    final_audio = AudioSegment.empty()

    async def synthesize_text(text, voice, out_path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, text in enumerate(lines):
            voice = voice_male if idx % 2 == 0 else voice_female
            filename = os.path.join(tmpdir, f"line_{idx:02d}.mp3")
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(synthesize_text(text, voice, filename))
                seg = AudioSegment.from_file(filename)
                final_audio += seg + AudioSegment.silent(duration=200)
            except Exception as e:
                print(f"❌ Error in /api/generate: {e}")
                traceback.print_exc()
                return jsonify({"error": str(e)}), 500

        buffer = BytesIO()
        final_audio.export(buffer, format="mp3", bitrate="64k")
        buffer.seek(0)

        # ✅ Encode audio to base64 và trả về cùng script
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
You are an IELTS listening question generator.

From the conversation below, create a Table Completion task for IELTS Listening Part 1.

✅ Determine the most suitable instruction (e.g. ONE WORD ONLY, A NUMBER, NO MORE THAN TWO WORDS...).
✅ Start with the instruction line.
✅ Then generate a table (in markdown) with two columns:
    - Column 1: Field label
    - Column 2: Correct answer (not blanks)
✅ Do NOT explain or wrap with code block.

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
