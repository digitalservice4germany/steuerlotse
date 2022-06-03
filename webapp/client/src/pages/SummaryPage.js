import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import StepForm from "../components/StepForm";
import SummaryComponent from "../components/SummaryComponent";
import { checkboxPropType } from "../lib/propTypes";
import { Headline1, Headline5 } from "../components/ContentPagesGeneralStyling";

export default function SummaryPage({
  plausibleDomain,
  form,
  fields,
  prevUrl,
  summaryData,
}) {
  const { t } = useTranslation();

  const plausibleProps = { method: "CTA Eingabe zu weiteren Einkünften" };

  const mandatorySummaryData = Object.values(summaryData.mandatoryData).map(
    (item, index) => <SummaryComponent key={index} {...item} />
  );

  const steuerminderungSummaryData = Object.values(
    summaryData.sectionSteuerminderung
  ).map((item, index) => <SummaryComponent key={index} {...item} />);

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <Headline1>{t("lotse.summary.heading")}</Headline1>
      <Headline5>{t("lotse.summary.mandatorySection")}</Headline5>
      {mandatorySummaryData}
      <Headline5>{t("lotse.summary.steuerminderungSection")}</Headline5>
      {steuerminderungSummaryData}
      <StepForm
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
        {...form}
      >
        <FormFieldConsentBox
          required
          autofocus
          fieldName="declaration_summary"
          fieldId="declaration_summary"
          checked={fields.confirmCompleteCorrect.checked}
          labelText={t("lotse.summary.confirmCompleteCorrect")}
          errors={fields.confirmCompleteCorrect.errors}
        />
      </StepForm>
    </>
  );
}

SummaryPage.propTypes = {
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  plausibleDomain: PropTypes.string,
  prevUrl: PropTypes.string.isRequired,
  fields: PropTypes.shape({
    confirmCompleteCorrect: checkboxPropType,
  }).isRequired,
  summaryData: PropTypes.shape({
    mandatoryData: PropTypes.arrayOf(
      PropTypes.shape({
        data: PropTypes.arrayOf(
          PropTypes.shape({
            name: PropTypes.string,
            value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
          })
        ).isRequired,
        label: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
      })
    ),
    sectionSteuerminderung: PropTypes.arrayOf(
      PropTypes.shape({
        data: PropTypes.arrayOf(
          PropTypes.shape({
            name: PropTypes.string,
            value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
          })
        ).isRequired,
        label: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
      })
    ),
  }).isRequired,
};
SummaryPage.defaultProps = {
  plausibleDomain: null,
};
