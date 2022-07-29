import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import StepNavButtons from "./StepNavButtons";
import { waitingMomentMessagePropType } from "../lib/propTypes";

export default function StepForm({
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

  function makeFetchCall(formData) {
    fetch(action, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((text, response) => {
        document.documentElement.innerHTML = text;
        console.log(response);
        // document.body.innerHTML = response.body;
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

StepForm.propTypes = {
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

StepForm.defaultProps = {
  ...StepNavButtons.defaultProps,
  sendDisableCall: undefined,
  waitingMessages: undefined,
  loadingFromOutside: false,
};
