import PropTypes from "prop-types";
import StepNavButtons from "./StepNavButtons";

export default function StepForm({
  children,
  action,
  csrfToken,
  explanatoryButtonText,
  showOverviewButton,
  nextButtonLabel,
}) {
  return (
    <form noValidate method="POST" action={action}>
      <input type="hidden" name="csrf_token" value={csrfToken} />
      {children}
      <StepNavButtons
        explanatoryButtonText={explanatoryButtonText}
        showOverviewButton={showOverviewButton}
        nextButtonLabel={nextButtonLabel}
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
};

StepForm.defaultProps = {
  ...StepNavButtons.defaultProps,
};
