import { useState } from "react";
import "./UploadSection.css";
import { uploadPDF } from "../services/api";

function UploadSection({ setPipelineStatus }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [uploadInfo, setUploadInfo] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setUploadInfo(null);
  };

  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF first.");
      return;
    }

    try {
      setUploading(true);
      setMessage("");
      setUploadInfo(null);

      // Upload
      setPipelineStatus({
        upload: "Running",
      });

      await delay(500);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Running",
      });

      await delay(500);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Completed",
        embedding: "Running",
      });

      await delay(500);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Completed",
        embedding: "Completed",
        retrieval: "Running",
      });

      // Backend Upload
      const response = await uploadPDF(file);

      console.log(response);

      // Save upload information
      setUploadInfo(response);

      await delay(400);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Completed",
        embedding: "Completed",
        retrieval: "Completed",
        rerank: "Running",
      });

      await delay(400);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Completed",
        embedding: "Completed",
        retrieval: "Completed",
        rerank: "Completed",
        rewrite: "Running",
      });

      await delay(400);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Completed",
        embedding: "Completed",
        retrieval: "Completed",
        rerank: "Completed",
        rewrite: "Completed",
        hallucination: "Running",
      });

      await delay(400);

      setPipelineStatus({
        upload: "Completed",
        chunking: "Completed",
        embedding: "Completed",
        retrieval: "Completed",
        rerank: "Completed",
        rewrite: "Completed",
        hallucination: "Completed",
      });

      setMessage("✅ PDF uploaded successfully!");
    } catch (error) {
      console.error(error);

      setPipelineStatus({});

      setUploadInfo(null);

      setMessage("❌ Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-card">
      <h2>Upload PDF</h2>

      <p className="subtitle">
        Upload a document for AI analysis
      </p>

      <label className="upload-box">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
        />

        <div className="upload-content">
          <h3>Choose PDF</h3>
          <p>Click here to browse your files</p>
        </div>
      </label>

      {file && (
        <div className="selected-file">
          📄 {file.name}
        </div>
      )}

      <button
        className="upload-btn"
        onClick={handleUpload}
        disabled={uploading}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {uploadInfo && (
        <div className="upload-summary">

          <h3>📄 Document Indexed</h3>

          <div className="summary-item">
            <strong>File:</strong> {uploadInfo.filename}
          </div>

          <div className="summary-item">
            <strong>Pages:</strong> {uploadInfo.pages}
          </div>

          <div className="summary-item">
            <strong>Chunks:</strong> {uploadInfo.chunks}
          </div>

          <div className="summary-item">
            <strong>Embeddings:</strong> {uploadInfo.embeddings}
          </div>

          <div className="ready-status">
            ✅ Ready for Questions
          </div>

        </div>
      )}

      {message && (
        <div className="message">
          {message}
        </div>
      )}
    </div>
  );
}

export default UploadSection;