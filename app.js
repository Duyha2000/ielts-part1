let currentScript = "";
let currentIndex = 0;
const audios = [];
const scripts = [];
let speedListenerAttached = false;

function togglePreview() {
  const preview = document.getElementById("scriptPreview");
  preview.style.display = preview.style.display === "none" ? "block" : "none";
}

function showScriptInput() {
  document.getElementById("dialogueWrapper").style.display = "block";
  document.getElementById("editScriptBtn").style.display = "none";
}

async function generateAudio() {
  const dialogueWrapper = document.getElementById("dialogueWrapper");
  const editBtn = document.getElementById("editScriptBtn");
  const textarea = document.getElementById("dialogueBox");
  const loading = document.getElementById("loadingMsg");
  const speedWrapper = document.getElementById("speedWrapper");
  const speedSelect = document.getElementById("speedControl");

  const text = textarea.value.trim();
  if (!text) return alert("Please enter a prompt or dialogue.");

  dialogueWrapper.style.display = "none";
  editBtn.style.display = "inline-block";
  loading.style.display = "block";
  speedWrapper.style.display = "none";

  const voiceMale = document.getElementById("voiceMale").value;
  const voiceFemale = document.getElementById("voiceFemale").value;
  const isPrompt = !text.includes("\n");

  try {
    const res = await fetch("https://ielts-part1.onrender.com/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: isPrompt ? "prompt" : "script",
        script: text,
        maleVoice: voiceMale,
        femaleVoice: voiceFemale,
      }),
    });

    loading.style.display = "none";

    if (!res.ok) {
      alert("❌ Failed to generate audio.");
      return;
    }

    const data = await res.json();
    currentScript = data.script;
    if (isPrompt) textarea.value = data.script;

    audios.length = 0;
    scripts.length = 0;

    data.audios.forEach((base64) => {
      const binary = atob(base64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }
      const blob = new Blob([bytes], { type: "audio/mpeg" });
      const url = URL.createObjectURL(blob);
      audios.push(url);
    });

    scripts.push(...data.scripts);
    speedWrapper.style.display = "inline-block";
    renderAudioPlayer(0);
  } catch (err) {
    loading.style.display = "none";
    alert("❌ Error: " + err.message);
    console.error(err);
  }
}

function renderAudioPlayer(index) {
  const container = document.getElementById("mainAudio");
  const scriptLabel = document.getElementById("scriptLabel");
  const preview = document.getElementById("scriptPreview");
  const speedSelect = document.getElementById("speedControl");

  container.innerHTML = "";
  preview.innerHTML = "";

  const audio = document.createElement("audio");
  audio.controls = true;
  audio.src = audios[index];
  audio.autoplay = true;
  audio.playbackRate = parseFloat(speedSelect.value);
  audio.classList.add("fadeIn");

  scriptLabel.innerText = `Script đoạn ${index + 1} / ${audios.length}`;
  scripts[index].forEach((line) => {
    const div = document.createElement("div");
    div.className = "bubble";
    div.innerText = line;
    preview.appendChild(div);
  });

  setTimeout(() => preview.scrollIntoView({ behavior: "smooth" }), 300);

  audio.addEventListener("ended", () => {
    archiveAudioPlayer(audio);
    currentIndex++;
    if (currentIndex < audios.length) {
      renderAudioPlayer(currentIndex);
    }
  });

  if (!speedListenerAttached) {
    speedSelect.addEventListener("change", () => {
      audio.playbackRate = parseFloat(speedSelect.value);
    });
    speedListenerAttached = true;
  }

  container.appendChild(audio);
}

function archiveAudioPlayer(audioEl) {
  const archive = document.getElementById("archiveAudios");
  audioEl.controls = true;
  audioEl.currentTime = 0;
  audioEl.pause();
  archive.appendChild(audioEl);
}

async function generateIELTSTable() {
  const script =
    currentScript || document.getElementById("dialogueBox").value.trim();
  if (!script) return alert("❌ No dialogue available to generate table.");

  const loading = document.getElementById("loadingMsg");
  const container = document.getElementById("ieltsTable");

  loading.style.display = "block";
  container.innerHTML = "";

  try {
    const res = await fetch(
      "https://ielts-part1.onrender.com/api/generate-table",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script }),
        mode: "cors",
      }
    );

    loading.style.display = "none";

    if (res.ok) {
      const { html } = await res.json();
      container.innerHTML = html;
    } else {
      container.innerHTML =
        "<p style='color:red'>❌ Failed to generate table.</p>";
    }
  } catch (err) {
    loading.style.display = "none";
    container.innerHTML =
      "<p style='color:red'>❌ Error: " + err.message + "</p>";
    console.error(err);
  }
}
