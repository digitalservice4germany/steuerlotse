import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormSuccessHeader from "../components/FormSuccessHeader";
import AnchorButton from "../components/AnchorButton";

// StepAck

export default function SubmitAcknowledgePage({ prevUrl, logoutUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("submitAcknowledge.successMessage"),
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormSuccessHeader {...stepHeader} />
      <h2 className="mt-5">{t("submitAcknowledge.next-steps.heading")}</h2>
      <p>{t("submitAcknowledge.next-steps.text")}</p>
      <h2 className="mt-5">{t("submitAcknowledge.logout.heading")}</h2>
      <p>{t("submitAcknowledge.logout.text1")}</p>
      <p>{t("submitAcknowledge.logout.text2")}</p>
      <AnchorButton url={logoutUrl} text={t("form.logout.button")} />
    </>
  );
}

SubmitAcknowledgePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
  logoutUrl: PropTypes.string.isRequired,
};
