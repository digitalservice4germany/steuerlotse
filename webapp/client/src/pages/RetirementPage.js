import React from "react";
import PropTypes from "prop-types";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import accordionRetirementPage from "../lib/RetirementPageFaqAnchors";
import { ContentWrapper } from "../components/ContentPagesGeneralStyling";
import AccordionComponent from "../components/AccordionComponent";
import CallToActionBox from "../components/CallToActionBox";
import retirementDates from "../lib/retirementDate";

export default function RetirementPage({ plausibleDomain }) {
  const { t } = useTranslation();

  const plausibleMethodRetirement = {
    method: "retirement",
  };

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          blogPostLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://digitalservice.bund.de/blog/steuerlotse-fuer-rente-und-pension-wird-eingestellt" />
          ),
        }}
        values={retirementDates}
      />
    );
  }

  const introText = (
    <>
      <p>{trans("retirementPage.formHeader.introOne")}</p>
      <p>{trans("retirementPage.formHeader.introTwo")}</p>
    </>
  );

  return (
    <>
      <ContentWrapper>
        <FormHeader
          title={t("retirementPage.formHeader.title")}
          intro={introText}
        />
        <AccordionComponent
          title={t("retirementPage.accordion.heading")}
          items={accordionRetirementPage}
          variant="marginTop"
          plausibleDomain={plausibleDomain}
        />
      </ContentWrapper>

      <CallToActionBox
        multipleButtons
        plausibleDomain={plausibleDomain}
        variant="outline"
        headline={t("retirementPage.questionBox.heading")}
        firstButtonText={t("retirementPage.questionBox.howItWorksButton.text")}
        firstButtonUrl="/sofunktionierts"
        firstButtonPlausibleGoal="So funktionierts"
        firstButtonPlausibleProps={plausibleMethodRetirement}
        secondButtonText={t("retirementPage.questionBox.helpButton.text")}
        secondButtonUrl="/hilfebereich"
        secondButtonPlausibleGoal="zum Hilfebereich"
        secondButtonPlausibleProps={plausibleMethodRetirement}
      />
    </>
  );
}

RetirementPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

RetirementPage.defaultProps = {
  plausibleDomain: undefined,
};
