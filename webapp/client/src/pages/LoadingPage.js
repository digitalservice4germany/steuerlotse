import React, { useState } from "react";
import ProgressBar from "react-bootstrap/ProgressBar";

export default function LoadingPage() {
  const [loadingPointer, setLoadingPointer] = useState(10);
  console.log(loadingPointer);
  // Funktion fürs polling
  function pollResult() {}

  return <ProgressBar now={80} />;
}
