import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormFailureHeader from "../components/FormFailureHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function UnlockCodeFailurePage({ prevUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("register.failure.header.title"),
    intro: t("register.failure.header.intro"),
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormFailureHeader {...stepHeader} />
    </>
  );
}

UnlockCodeFailurePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
