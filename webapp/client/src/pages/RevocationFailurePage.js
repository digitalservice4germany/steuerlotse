import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFailureHeader from "../components/FormFailureHeader";

export default function RevocationFailurePage({ prevUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("revocation.failure.header.title"),
    intro: t("revocation.failure.header.intro"),
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormFailureHeader {...stepHeader} />
    </>
  );
}

RevocationFailurePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
