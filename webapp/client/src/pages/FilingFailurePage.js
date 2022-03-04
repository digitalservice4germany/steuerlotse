import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import AnchorButton from "../components/AnchorButton";
import DisplayFailureIcon from "../components/DisplayFailureIcon";

export default function FilingFailurePage({ errorDetails }) {
  const { t } = useTranslation();
  const mail = t("filing.failure.nextStep.text.mail");
  const mailto = `mailto:${mail}`;
  return (
    <>
      <StepHeaderButtons />
      <DisplayFailureIcon
        title={t("filing.failure.alert.title")}
        errorDetails={errorDetails}
      />
      <div className="spacing-b-04">
        <h2 className="h4 mt-5">{t("filing.failure.nextStep.heading")}</h2>
        <p className="mb-4 result-text">
          {t("filing.failure.nextStep.text.before")}
          <a href={mailto}>{mail}</a>
          {t("filing.failure.nextStep.text.after")}
        </p>
      </div>
      <div className="spacing-b-11 row m-0">
        <AnchorButton text={t("filing.failure.textUs")} url={mailto} />
      </div>
    </>
  );
}

FilingFailurePage.propTypes = {
  errorDetails: PropTypes.arrayOf(PropTypes.string),
};

FilingFailurePage.defaultProps = {
  errorDetails: [
    "Das Geburtsjahr liegt nach dem Veranlagungszeitraum (steuerpflichtige Person / Ehemann / Person A).",
  ],
};
