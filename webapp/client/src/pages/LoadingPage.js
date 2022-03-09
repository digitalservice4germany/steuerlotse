import React, { useEffect, useState } from "react";
import ProgressBar from "react-bootstrap/ProgressBar";
import PropTypes from "prop-types";
import StepHeaderButtons from "../components/StepHeaderButtons";

const randomId = new Date().getTime();
let continueBar = true;

export default function LoadingPage({ status, delay }) {
  const [progress, setProgress] = useState(0);
  const [processStatus, setProcessStatus] = useState("processing");
  const [counter, setCounter] = useState(0);
  const [visible, setVisible] = useState(false);
  const [timer, setTimer] = useState(0);

  function loadSuccess() {
    document.getElementById("success").click();
  }

  function loadFailure() {
    document.getElementById("failed").click();
  }

  function sleep(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  }

  useEffect(() => {
    async function fetchData() {
      console.log(
        `Making call: http://localhost:3000/get_dummy_job/${status}/${delay}/${randomId}`
      );
      const result = await fetch(
        `http://localhost:3000/get_dummy_job/${status}/${delay}/${randomId}`
      )
        .then((response) => response.json())
        .then((responseJson) => responseJson);
      const processStatusResponse = result.processStatus;
      console.log(`Status: ${processStatusResponse}`);
      switch (processStatusResponse) {
        case "processing":
          setCounter(counter + 1);
          break;
        case "success":
          setProgress(100);
          await sleep(500);
          loadSuccess();
          break;
        case "failure":
          continueBar = false;
          loadFailure();
          break;
        default:
      }
      setProcessStatus(processStatusResponse);
    }

    if (processStatus === "processing") {
      fetchData();
    }
  }, [status, delay, visible, counter, processStatus]);

  useEffect(() => {
    console.log(`Progress: ${progress}`);
    let interval;
    if (progress < 100 && continueBar) {
      interval = setInterval(() => {
        setProgress((prev) => prev + 10 / 60);
      }, 100);
    }
    return () => clearInterval(interval);
  }, [progress]);

  useEffect(() => {
    let interval;
    if (timer < 8) {
      interval = setInterval(() => {
        setTimer((prev) => prev + 1);
      }, 1000);
    } else {
      setVisible(true);
    }
    return () => clearInterval(interval);
  }, [visible, timer]);

  return (
    <>
      <StepHeaderButtons />
      <h1 className="my-4">Ihre Steuererklärung wird verschickt.</h1>
      <ProgressBar now={progress} />
      <p
        style={{
          marginTop: "10px",
          visibility: visible ? "visible" : "hidden",
        }}
      >
        Bitte lassen Sie während des Ladevorgangs diese Seite geöffnet.
      </p>
      <a id="success" style={{ visibility: "hidden" }} href="/lotse/step/ack">
        Blabla
      </a>
      <a
        id="failed"
        style={{ visibility: "hidden" }}
        href="/unlock_code_request/step/unlock_code_failure"
      >
        Blabla
      </a>
    </>
  );
}

LoadingPage.propTypes = {
  status: PropTypes.string.isRequired,
  delay: PropTypes.number.isRequired,
};
