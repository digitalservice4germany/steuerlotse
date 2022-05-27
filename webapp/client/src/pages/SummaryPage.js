import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import { ContentWrapper } from "../components/ContentPagesGeneralStyling";
import StepHeaderButtons from "../components/StepHeaderButtons";
// import SummaryComponent from "../components/SummaryComponent";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import StepForm from "../components/StepForm";
import SummaryComponent from "../components/SummaryComponent";

const Headline1 = styled.h1`
  font-size: var(--text-4xl);
  margin-top: var(--spacing-05);
  margin-bottom: 0;
`;

const Headline2 = styled.h2`
  font-size: var(--text-medium-big);
  margin-top: var(--spacing-08);
  margin-bottom: 0;
`;

export default function SummaryPage({
  plausibleDomain,
  form,
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
      <Headline2>{t("lotse.summary.mandatorySection")}</Headline2>
      {mandatorySummaryData}
      <Headline2>{t("lotse.summary.steuerminderungSection")}</Headline2>
      {steuerminderungSummaryData}
      <StepForm
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
        {...form}
      >
        <FormFieldConsentBox
          required
          fieldName="declaration_summary"
          fieldId="declaration_summary"
          // checked={fields.declarationIncomes.checked}
          labelText={t("lotse.summary.declarationConfirmation")}
          // errors={fields.declarationIncomes.errors}
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
  test: PropTypes.string.isRequired,
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

// array in prop types of the information
// loop within the summary page
// output what looks like
// never render text in the front end for this - this has to be dynamic

SummaryPage.defaultProps = {
  plausibleDomain: null,
};
