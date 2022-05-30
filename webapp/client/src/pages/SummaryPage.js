import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import StepForm from "../components/StepForm";
import SummaryComponent from "../components/SummaryComponent";
import { checkboxPropType } from "../lib/propTypes";
import {
  ContentWrapper,
  Headline1,
  Headline5,
} from "../components/ContentPagesGeneralStyling";

export default function SummaryPage({
  plausibleDomain,
  form,
  fields,
  prevUrl,
  summaryData,
}) {
  const { t } = useTranslation();

  const plausibleProps = { method: "CTA Eingabe zu weiteren Einkünften" };

  const mandatorySummaryData = Object.values(
    summaryData.section_steps.mandatory_data.data
  ).map((item) => <SummaryComponent data={item} />);

  const steuerminderungSummaryData = Object.values(
    summaryData.section_steps.section_steuerminderung.data
  ).map((item) => <SummaryComponent data={item} />);

  return (
    <ContentWrapper>
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
          checked={fields.declarationSummary.checked}
          labelText={t("lotse.summary.declarationConfirmation")}
          errors={fields.declarationSummary.errors}
        />
      </StepForm>
    </ContentWrapper>
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
  fields: PropTypes.exact({
    declarationSummary: checkboxPropType,
  }).isRequired,
  summaryData: PropTypes.exact({
    section_steps: {
      madatory_data: {
        data: {
          decl_incomes: {
            data: {},
            label: PropTypes.string,
            url: PropTypes.string,
          },
          decl_edaten: {
            data: {},
            label: PropTypes.string,
            url: PropTypes.string,
          },
          familienstand: {
            data: {},
            label: PropTypes.string,
            url: PropTypes.string,
          },
          steuernummer: {
            data: {},
            label: PropTypes.string,
            url: PropTypes.string,
          },
        },
      },
    },
  }).isRequired,
};
SummaryPage.defaultProps = {
  plausibleDomain: null,
};
