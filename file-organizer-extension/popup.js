const API = "http://127.0.0.1:5000";

document.getElementById("organizeBtn").addEventListener("click", organize);
document.getElementById("statsBtn").addEventListener("click", stats);
document.getElementById("undoBtn").addEventListener("click", undo);

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("folderPicker");

let selectedFiles = [];

function setStatus(text, type = "") {
    const el = document.getElementById("status");
    el.textContent = text;
    el.className = "status " + type;
}

function setProgress(val) {
    document.getElementById("progressBar").style.width = val + "%";
}

function showOutput(data) {
    document.getElementById("out").textContent =
        JSON.stringify(data, null, 2);
}

function getFiles() {
    return selectedFiles;
}

function updateFileCountUI() {
    dropZone.innerHTML = selectedFiles.length
        ? `📦 ${selectedFiles.length} files loaded`
        : `Drop folder here or click to select`;
}

/* =========================
   FILE INPUT HANDLING
========================= */

fileInput.addEventListener("change", (e) => {
    selectedFiles = [...e.target.files].map(f => ({
        name: f.name,
        type: f.type,
        size: f.size
    }));

    updateFileCountUI();
    setStatus(`${selectedFiles.length} files ready ✨`, "success");
});

/* =========================
   DRAG & DROP HANDLING
========================= */

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");

    selectedFiles = [...e.dataTransfer.files].map(f => ({
        name: f.name,
        type: f.type,
        size: f.size
    }));

    updateFileCountUI();
    setStatus(`${selectedFiles.length} files ready ✨`, "success");
});

/* =========================
   MAIN ACTIONS
========================= */

async function organize() {
    try {
        if (!selectedFiles.length) {
            setStatus("No files selected 💀", "error");
            return;
        }

        setProgress(20);
        setStatus("Scanning files...", "loading");

        const res = await fetch(`${API}/organize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ files: selectedFiles })
        });

        setProgress(70);

        const data = await res.json();

        setProgress(100);
        setStatus("Preview ready ✨", "success");

        showOutput(data.plan);

    } catch (err) {
        setStatus("Backend error 💀", "error");
        showOutput({ error: err.message });
    }
}

async function stats() {
    try {
        if (!selectedFiles.length) {
            setStatus("No files selected 💀", "error");
            return;
        }

        setProgress(30);
        setStatus("Analyzing...");

        const res = await fetch(`${API}/stats`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ files: selectedFiles })
        });

        const data = await res.json();

        setProgress(100);
        setStatus("Done ✨", "success");

        showOutput(data.stats);

    } catch (err) {
        setStatus("Error 💀", "error");
        showOutput({ error: err.message });
    }
}

async function undo() {
    try {
        setProgress(50);
        setStatus("Reverting...");

        const res = await fetch(`${API}/undo`, {
            method: "POST"
        });

        const data = await res.json();

        setProgress(100);
        setStatus("Undone ↩️", "success");

        showOutput(data);

    } catch (err) {
        setStatus("Error 💀", "error");
        showOutput({ error: err.message });
    }
}