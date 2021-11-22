import PropTypes from "prop-types";
import React from "react";
import FormSuccessHeader from "../components/FormSuccessHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";
import StepNavButtons from "../components/StepNavButtons";

export default function RevocationSuccessPage({
  stepHeader,
  prevUrl,
  nextUrl,
}) {
  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormSuccessHeader {...stepHeader} />
      <StepNavButtons nextUrl={nextUrl} isForm={false} />
    </>
  );
}

RevocationSuccessPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  nextUrl: PropTypes.string.isRequired,
};
