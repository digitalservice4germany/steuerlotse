import React, { useEffect, useState } from "react";
import ProgressBar from "react-bootstrap/ProgressBar";

let interval;

export default function LoadingPage() {
  // Funktion fürs polling
  function pollResult() {
    fetch("http://localhost:3000/get_dummy_job/1")
      .then((response) => response.json())
      .then((data) => console.log(data));
  }
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    pollResult();

    if (progress <= 100) {
      interval = setInterval(() => {
        setProgress((prev) => prev + 1);
      }, 100);
    } else {
      clearInterval(interval);
    }
  });

  return <ProgressBar now={progress} />;
}
