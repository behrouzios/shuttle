import React, { useState } from "react";
import axios from "axios";

const UploadFile = ({ setMessage }) => {
  const [file, setFile] = useState(null);
  const [uploadedData, setUploadedData] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) {
      setMessage("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = localStorage.getItem("authToken");
      const response = await axios.post(
        "http://127.0.0.1:8000/core/upload-file/",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setMessage("File uploaded successfully!");
      setUploadedData(response.data.data); // Capture uploaded file data
    } catch (error) {
      console.error("Error occurred during file upload:", error);
      const errorMessage =
        error.response?.data?.error || "An error occurred. Please try again.";
      setMessage(errorMessage);
    }
  };

  return (
    <div>
      <h3>Upload CSV File</h3>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload File</button>
      <div>
        {uploadedData && (
          <div>
            <h4>Uploaded Data:</h4>
            <table border="1" cellPadding="10">
              <thead>
                <tr>
                  {/* Dynamically create table headers */}
                  {Object.keys(uploadedData[0]).map((key, index) => (
                    <th key={index}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Render each row of data */}
                {uploadedData.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {Object.values(row).map((value, colIndex) => (
                      <td key={colIndex}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadFile;
