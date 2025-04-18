from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import traceback
from pydub import AudioSegment
import tempfile, os
from io import BytesIO
import edge_tts
import asyncio

# Flask app setup
app = Flask(__name__)

CORS(app, resources={r"/api/*": {
    "origins": [
        "https://ieltspart1.netlify.app",
        "https://www.ieltspart1.netlify.app"
    ],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"],
}})

@app.route("/api/generate", methods=["POST"])
def generate_audio():
    data = request.get_json()
    script = data.get("script", "")
    if not script:
        return jsonify({"error": "No script provided"}), 400

    lines = [line.strip() for line in script.strip().split("\n") if line.strip()]
    final_audio = AudioSegment.empty()

    async def synthesize_text(text, voice, out_path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Sử dụng tệp tạm thời cho từng đoạn âm thanh
        for idx, text in enumerate(lines):
            speaker = "male" if idx % 2 == 0 else "female"
            voice_male = data.get("maleVoice", "en-US-GuyNeural")
            voice_female = data.get("femaleVoice", "en-US-JennyNeural")
            voice = voice_male if speaker == "male" else voice_female

            filename = os.path.join(tmpdir, f"line_{idx:02d}.mp3")
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(synthesize_text(text, voice, filename))
                seg = AudioSegment.from_file(filename)
                
                # Sau khi tạo âm thanh từ tệp, bạn có thể lưu hoặc xử lý từng đoạn một
                final_audio += seg + AudioSegment.silent(duration=500)

                # Nếu không muốn giữ tất cả trong bộ nhớ, bạn có thể lưu đoạn âm thanh ra tệp
                temp_filename = os.path.join(tmpdir, f"final_segment_{idx:02d}.mp3")
                final_audio.export(temp_filename, format="mp3")

                # Sau khi xuất tạm, reset để xử lý đoạn tiếp theo
                final_audio = AudioSegment.empty()

            except Exception as e:
                print(f"❌ Error in /api/generate: {e}")
                traceback.print_exc()
                return jsonify({"error": str(e)}), 500

        # Sau khi tất cả các đoạn âm thanh đã được xuất tạm, kết hợp lại nếu cần thiết
        buffer = BytesIO()
        final_audio.export(buffer, format="mp3")
        buffer.seek(0)
        return send_file(buffer, mimetype="audio/mpeg", download_name="final.mp3")

if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False, host='0.0.0.0', port=5000)
