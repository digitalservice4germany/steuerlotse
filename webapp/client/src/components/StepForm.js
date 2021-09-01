import PropTypes from "prop-types";
import FormNavButtons from "./FormNavButtons";

export default function StepForm({
  submitUrl,
  csrfToken,
  explanatoryButtonText,
  overviewButton,
  nextButtonLabel,
}) {
  return (
    <form
      noValidate
      className="container px-0 form-container"
      method="POST"
      action={submitUrl}
    >
      <input type="hidden" name="csrf_token" value={csrfToken} />
      <FormNavButtons
        explanatoryButtonText={explanatoryButtonText}
        overviewButton={overviewButton}
        nextButtonLabel={nextButtonLabel}
      />
    </form>
  );
}

StepForm.propTypes = {
  submitUrl: PropTypes.string,
  overviewButton: PropTypes.bool,
  csrfToken: PropTypes.string,
  explanatoryButtonText: PropTypes.string,
  nextButtonLabel: PropTypes.string,
};
