import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";
import StepForm from "../components/StepForm";

export default function NoPauschbetragPage({ stepHeader, form, prevUrl }) {
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
      <StepForm {...form} />
    </>
  );
}

NoPauschbetragPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
