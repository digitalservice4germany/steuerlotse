import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";
import StepNavButtons from "../components/StepNavButtons";

export default function NoPauschbetragPage({
  stepHeader,
  showOverviewButton,
  overviewUrl,
  prevUrl,
  nextUrl,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={[
          t("lotse.noPauschbetrag.intro.p1"),
          <Trans
            t={t}
            i18nKey="lotse.noPauschbetrag.intro.p2"
            components={{
              bold: <b />,
            }}
          />,
        ]}
      />
      <StepNavButtons
        isForm={false}
        nextUrl={nextUrl}
        showOverviewButton={showOverviewButton}
        overviewUrl={overviewUrl}
      />
    </>
  );
}

NoPauschbetragPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  nextUrl: PropTypes.string.isRequired,
  showOverviewButton: PropTypes.bool.isRequired,
  overviewUrl: PropTypes.string.isRequired,
};
