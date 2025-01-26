import React, { useState } from "react";
import axios from "axios";

function App() {
  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!allowedTypes.includes(file.type)) {
      setError("Invalid file type. Please upload a PDF or DOCX file.");
      return;
    }

    // Clear previous errors
    setError("");

    // Upload file to backend
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFiles([...files, response.data]);
    } catch (err) {
      setError("Failed to upload file. Please try again.");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/delete/${id}`);
      setFiles(files.filter((file) => file.id !== id));
    } catch (err) {
      setError("Failed to delete file. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-center mb-8">Document Management System</h1>
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <input
          type="file"
          onChange={handleFileUpload}
          className="mb-4"
          accept=".pdf,.docx"  // Allow both PDF and DOCX files
        />
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <ul>
          {files.map((file) => (
            <li key={file.id} className="flex justify-between items-center mb-2">
              <div>
                <p className="font-semibold">{file.title}</p>
                <p className="text-sm text-gray-500">{file.uploadDate}</p>
                <p className="text-sm text-gray-500">{file.category}</p>
                <p className="text-sm text-gray-500">{file.summary}</p>
              </div>
              <button
                onClick={() => handleDelete(file.id)}
                className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;