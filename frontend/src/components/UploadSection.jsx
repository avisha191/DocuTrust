import { useState } from "react";
import API from "../services/api";

function UploadSection() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      await API.post("/upload", formData);
      alert("PDF Uploaded Successfully");
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
}

export default UploadSection;