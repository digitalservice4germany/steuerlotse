import PropTypes from "prop-types";
import FormNavButtons from "./FormNavButtons";

export default function StepForm({
  children,
  action,
  csrfToken,
  explanatoryButtonText,
  showOverviewButton,
  nextButtonLabel,
}) {
  return (
    <form
      noValidate
      className="container px-0 form-container"
      method="POST"
      action={action}
    >
      <input type="hidden" name="csrf_token" value={csrfToken} />
      {children}
      <FormNavButtons
        explanatoryButtonText={explanatoryButtonText}
        showOverviewButton={showOverviewButton}
        nextButtonLabel={nextButtonLabel}
      />
    </form>
  );
}

StepForm.propTypes = {
  children: PropTypes.node.isRequired,
  action: PropTypes.string.isRequired,
  csrfToken: PropTypes.string.isRequired,
  showOverviewButton: PropTypes.bool,
  explanatoryButtonText: PropTypes.string,
  nextButtonLabel: PropTypes.string,
};

StepForm.defaultProps = {
  ...FormNavButtons.defaultProps,
};
