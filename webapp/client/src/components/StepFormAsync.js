import PropTypes from "prop-types";
import { React, useEffect, useState } from "react";
import StepNavButtons from "./StepNavButtons";
import { waitingMomentMessagePropType } from "../lib/propTypes";

export default function StepFormAsync({
  children,
  action,
  csrfToken,
  explanatoryButtonText,
  showOverviewButton,
  nextButtonLabel,
  plausibleGoal,
  plausibleDomain,
  plausibleProps,
  sendDisableCall,
  waitingMessages,
  loadingFromOutside,
}) {
  const [loading, setLoading] = useState(loadingFromOutside);
  // eslint-disable-next-line no-promise-executor-return
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));

  async function makeFetchCall(formData) {
    const startTime = Date.now();

    fetch(action, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        const durationTime = Date.now();
        const duration = (durationTime - startTime) / 1000;
        const minDuration = 2000;

        if (duration < minDuration) {
          return Promise.resolve(delay(minDuration - duration)).then(
            () => response
          );
        }

        return response;
      })
      .then((response) => {
        if (response.ok) {
          return response.text();
        }
        return Promise.reject(response);
      })
      .then((text) => {
        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(text, "text/html");
        document.body.innerHTML = htmlDoc.body.innerHTML;
        window.renderReact();
      })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() => {
    if (loadingFromOutside) {
      const form = document.getElementById("theForm");

      Array.from(form.elements)
        .filter((element) => element.hasAttribute("required"))
        .forEach((filteredElement) => {
          filteredElement.removeAttribute("disabled");
        });
      const formData = new FormData(form);
      makeFetchCall(formData);
    }
  }, []);

  function sendDisableCallAndFetch(event) {
    event.preventDefault();
    const { target } = event;

    const formData = new FormData(target);

    if (sendDisableCall !== undefined) {
      setLoading(true);
      sendDisableCall();
    }

    makeFetchCall(formData);
  }

  return (
    <form id="theForm" noValidate onSubmit={sendDisableCallAndFetch}>
      <input type="hidden" name="csrf_token" value={csrfToken} />
      {children}
      <StepNavButtons
        explanatoryButtonText={explanatoryButtonText}
        showOverviewButton={showOverviewButton}
        nextButtonLabel={nextButtonLabel}
        plausibleGoal={plausibleGoal}
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
        loading={loading}
        waitingMessages={waitingMessages}
      />
    </form>
  );
}

StepFormAsync.propTypes = {
  children: PropTypes.node,
  action: PropTypes.string.isRequired,
  csrfToken: PropTypes.string.isRequired,
  showOverviewButton: PropTypes.bool,
  explanatoryButtonText: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
  ]),
  nextButtonLabel: PropTypes.string,
  plausibleGoal: PropTypes.string,
  plausibleProps: PropTypes.shape({ method: PropTypes.string }),
  plausibleDomain: PropTypes.string,
  sendDisableCall: PropTypes.any,
  waitingMessages: waitingMomentMessagePropType,
  loadingFromOutside: PropTypes.bool,
};

StepFormAsync.defaultProps = {
  ...StepNavButtons.defaultProps,
  sendDisableCall: undefined,
  waitingMessages: undefined,
  loadingFromOutside: false,
};
