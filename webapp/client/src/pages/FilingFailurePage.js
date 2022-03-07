import React from "react";
import PropTypes from "prop-types";
import { Trans, useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import AnchorButton from "../components/AnchorButton";
import FailureMessageBox from "../components/FailureMessageBox";

export default function FilingFailurePage({ errorDetails }) {
  const { t } = useTranslation();
  const mailto = t("filing.failure.nextStep.mailto");
  return (
    <>
      <StepHeaderButtons />
      <FailureMessageBox
        title={t("filing.failure.alert.title")}
        errorDetails={errorDetails}
      />
      <div className="spacing-b-04">
        <h2 className="h4 mt-5">{t("filing.failure.nextStep.heading")}</h2>
        <p className="mb-4 result-text">
          <Trans
            t={t}
            i18nKey="filing.failure.nextStep.text"
            components={{
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              anchormail: <a href={mailto} />,
            }}
          />
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
  errorDetails: [],
};
