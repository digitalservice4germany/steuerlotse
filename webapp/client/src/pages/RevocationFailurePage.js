import PropTypes from "prop-types";
import React from "react";
import FailurePage from "../components/FailurePage";

export default function RevocationFailurePage({ prevUrl }) {
  return <FailurePage useCase="revocation" prevUrl={prevUrl} />;
}

RevocationFailurePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
