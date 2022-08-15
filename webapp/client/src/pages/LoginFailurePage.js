import PropTypes from "prop-types";
import React from "react";
import FailurePage from "../components/FailurePage";

export default function LoginFailurePage({ prevUrl }) {
  return <FailurePage useCase="unlockCodeActivation" prevUrl={prevUrl} />;
}

LoginFailurePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
