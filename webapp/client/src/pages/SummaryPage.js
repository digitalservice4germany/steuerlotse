import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import { ContentWrapper } from "../components/ContentPagesGeneralStyling";
import StepHeaderButtons from "../components/StepHeaderButtons";
import SummaryComponent from "../components/SummaryComponent";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import StepForm from "../components/StepForm";

const Headline1 = styled.h1`
  font-size: var(--text-4xl);
  margin-bottom: var(--spacing-05);
`;

const Headline2 = styled.h2`
  font-size: var(--text-medium-big);
  margin-top: var(--spacing-08);
`;

export default function SummaryPage({ plausibleDomain, form, prevUrl }) {
  const { t } = useTranslation();
  const plausibleProps = { method: "CTA Eingabe zu weiteren Einkünften" };

  return (
    <ContentWrapper>
      <StepHeaderButtons url={prevUrl} />
      <Headline1>{t("lotse.summary.heading")}</Headline1>
      <Headline2>{t("lotse.summary.mandatoryHeading")}</Headline2>
      <SummaryComponent stepLabel stepLink label value />
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
};

// array in prop types of the information
// loop within the summary page
// output what looks like
// never render text in the front end for this - this has to be dynamic

SummaryPage.defaultProps = {
  plausibleDomain: null,
};
