import PropTypes from "prop-types";
import React from "react";
import FormSuccessHeader from "../components/FormSuccessHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function RevocationSuccessPage({ stepHeader }) {
  return (
    <>
      <StepHeaderButtons />
      <FormSuccessHeader {...stepHeader} />
    </>
  );
}

RevocationSuccessPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
};
