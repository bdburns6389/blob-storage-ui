import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [blobs, setBlobs] = useState([]);

  useEffect(() => {
    const fetchBlobs = async () => {
      const result = await axios("/list");
      console.log(result.data.blobs);
      setBlobs(result.data.blobs);
    };
    fetchBlobs();
  }, []);

  const downloadClick = (filename) => {
    console.log("hello");
    fetch(`/download/${filename}`)
      // Convert data into a 'blob'.
      .then((res) => res.blob())
      .then((blob) => {
        // Create blob link for download.
        const filenameWithoutFolder = filename.split("/").pop();
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filenameWithoutFolder);

        // Append to html page.
        document.body.appendChild(link);

        // Force download.
        link.click();

        // Clean up and remove link from dom.
        link.parentNode.removeChild(link);
      });
  };

  return (
    <div className="App">
      {blobs.length > 0 &&
        blobs.map((blob) => (
          <h2 style={{ textAlign: "left" }}>
            {blob}
            <button onClick={() => downloadClick(blob)}>Download</button>
          </h2>
        ))}
    </div>
  );
}

export default App;
