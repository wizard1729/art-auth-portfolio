import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [profile, setProfile] = useState("default");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeArtwork = async () => {
    if (!file) return alert("Upload artwork first");

    setLoading(true);
    const form = new FormData();
    form.append("file", file);

    const res = await fetch(
      `${API}/analyze/report?profile=${profile}`,
      { method: "POST", body: form }
    );

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🎨 Art Authentication Dashboard</h1>

      <div className="card">
        <input type="file" onChange={e => setFile(e.target.files[0])} />

        <select onChange={e => setProfile(e.target.value)}>
          <option value="default">Default</option>
          <option value="modern">Modern</option>
          <option value="renaissance">Renaissance</option>
          <option value="contemporary">Contemporary</option>
        </select>

        <button onClick={analyzeArtwork}>
          {loading ? "Analyzing..." : "Analyze Artwork"}
        </button>
      </div>

      {result && (
        <div className="result">
          <h2>Decision Result</h2>

          <p>
            <strong>Confidence Index:</strong>{" "}
            <span className={`band ${result.confidence_band}`}>
              {result.confidence_index}% ({result.confidence_band})
            </span>
          </p>

          <a href={result.report_url} target="_blank">
            📄 Download PDF Report
          </a>
        </div>
      )}
    </div>
  );
}
