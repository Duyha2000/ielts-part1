from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import traceback
from pydub import AudioSegment
import tempfile, os
from io import BytesIO
import edge_tts
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

# Flask app setup
app = Flask(__name__)

# Enable CORS for specific origins
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://ieltspart1.netlify.app",
        "https://www.ieltspart1.netlify.app"
    ],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"],
}})

# Load environment variables
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/api/generate", methods=["POST"])
def generate_audio():
    # Get the input data from the request
    data = request.get_json()
    script = data.get("script", "")
    
    if not script:
        return jsonify({"error": "No script provided"}), 400

    # Split the script into lines and clean up whitespace
    lines = [line.strip() for line in script.strip().split("\n") if line.strip()]

    async def synthesize_text(text, voice, out_path):
        """Generate the audio for the provided text and save to the specified path"""
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(out_path)
            print(f"Audio saved to {out_path}")  # Debugging log to confirm audio creation
        except Exception as e:
            print(f"Error during audio synthesis: {e}")
            raise

    # Create a temporary directory for audio files
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, text in enumerate(lines):
            speaker = "male" if idx % 2 == 0 else "female"
            voice_male = data.get("maleVoice", "en-US-GuyNeural")
            voice_female = data.get("femaleVoice", "en-US-JennyNeural")
            voice = voice_male if speaker == "male" else voice_female

            filename = os.path.join(tmpdir, f"line_{idx:02d}.mp3")
            try:
                # Create the audio for this line
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(synthesize_text(text, voice, filename))

                # Load the audio segment from the generated file
                seg = AudioSegment.from_file(filename)

                # Streaming each part of the audio instead of loading everything into memory
                buffer = BytesIO()
                seg.export(buffer, format="mp3")
                buffer.seek(0)

                # Stream the file directly to the user part by part
                return send_file(buffer, mimetype="audio/mpeg", download_name="final.mp3", as_attachment=True)

            except Exception as e:
                print(f"❌ Error processing line {idx+1}: {e}")
                traceback.print_exc()
                return jsonify({"error": str(e)}), 500

@app.route("/api/generate-table", methods=["POST"])
def generate_ielts_table():
    # Get the input data from the request
    data = request.get_json()
    script = data.get("script", "")
    
    if not script:
        return jsonify({"error": "Missing script"}), 400

    try:
        # Generate the prompt for OpenAI based on the input script
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

        # Call OpenAI's API to generate the IELTS table task
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the markdown table from the response
        markdown_table = response.choices[0].message.content

        # Convert the markdown table to HTML for rendering
        html = convert_markdown_table_to_tooltip_html(markdown_table)
        return jsonify({"html": html})

    except Exception as e:
        print(f"❌ Error generating IELTS table: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def convert_markdown_table_to_tooltip_html(md_table):
    """Convert the markdown table into HTML with tooltips for the answers"""
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

    # Build the HTML table
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
    """Set CORS headers for all responses"""
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False, host='0.0.0.0', port=5000)
