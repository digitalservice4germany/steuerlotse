import PropTypes from "prop-types";
import React from "react";
import FormHeader from "../components/FormHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function LoginPage({
  prevUrl,
  backLinkText,
  stepTitle,
  stepIntro,
}) {
  return (
    <React.Fragment>
      <StepHeaderButtons backLinkUrl={prevUrl} backLinkText={backLinkText} />
      <FormHeader title={stepTitle} intro={stepIntro} />
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
};

LoginPage.defaultProps = {
  prevUrl: null,
  // TODO: intl
  backLinkText: "form.back",
};
