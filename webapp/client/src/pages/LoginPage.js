import PropTypes from "prop-types";
import React from "react";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function LoginPage({
  prevUrl,
  backLinkText,
  stepTitle,
  stepIntro,
  submitUrl,
  overviewButton,
  csrfToken,
  explanatoryButtonText,
  nextButtonLabel,
}) {
  return (
    <React.Fragment>
      <StepHeaderButtons backLinkUrl={prevUrl} backLinkText={backLinkText} />
      <FormHeader title={stepTitle} intro={stepIntro} />
      <StepForm
        {...{
          submitUrl,
          overviewButton,
          csrfToken,
          explanatoryButtonText,
          nextButtonLabel,
        }}
      />
    </React.Fragment>
  );
}

LoginPage.propTypes = {
  // render_info.prev_url
  prevUrl: PropTypes.string,
  // render_info.back_link_text
  backLinkText: PropTypes.string,
  // render_info.step_title
  stepTitle: PropTypes.string,
  // render_info.step_intro
  stepIntro: PropTypes.string,
  // render_info.submit_url
  submitUrl: PropTypes.string,
  // !!render_info.overview_url
  overviewButton: PropTypes.string,
  // csrf_token()
  csrfToken: PropTypes.string,
  // explanatory_button_text
  explanatoryButtonText: PropTypes.string,
  // render_info.additional_info.next_button_label
  nextButtonLabel: PropTypes.string,
};

LoginPage.defaultProps = {
  prevUrl: null,
  // TODO: intl
  backLinkText: "form.back",
};
