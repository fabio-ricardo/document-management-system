import os

# Define the folder structure
frontend_folder = "frontend"
public_folder = os.path.join(frontend_folder, "public")
src_folder = os.path.join(frontend_folder, "src")
components_folder = os.path.join(src_folder, "components")
styles_folder = os.path.join(src_folder, "styles")

# Create folders
os.makedirs(public_folder, exist_ok=True)
os.makedirs(src_folder, exist_ok=True)
os.makedirs(components_folder, exist_ok=True)
os.makedirs(styles_folder, exist_ok=True)

# Create package.json
package_json = """
{
  "name": "document-management-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.5.0",
    "tailwindcss": "^3.3.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
"""
with open(os.path.join(frontend_folder, "package.json"), "w") as f:
    f.write(package_json)

# Create tailwind.config.js
tailwind_config = """
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
with open(os.path.join(frontend_folder, "tailwind.config.js"), "w") as f:
    f.write(tailwind_config)

# Create public/index.html
index_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document Management System</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""
with open(os.path.join(public_folder, "index.html"), "w") as f:
    f.write(index_html)

# Create src/index.css
index_css = """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""
with open(os.path.join(src_folder, "index.css"), "w") as f:
    f.write(index_css)

# Create src/index.js
index_js = """
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
with open(os.path.join(src_folder, "index.js"), "w") as f:
    f.write(index_js)

# Create src/App.js
app_js = """
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.includes("pdf") && !file.type.includes("docx")) {
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
          accept=".pdf,.docx"
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
"""
with open(os.path.join(src_folder, "App.js"), "w") as f:
    f.write(app_js)

# Create setup instructions
readme = """
# Document Management System - Frontend

## Setup Instructions

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and visit `http://localhost:3000` to view the application.
"""
with open(os.path.join(frontend_folder, "README.md"), "w") as f:
    f.write(readme)

print("Frontend code and files generated successfully!")
