import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import {
  accordionCanIUseSection,
  letterActivationCodeSection,
  submitTaxReturnSection,
  afterSubmissionSection,
} from "../lib/helperPageFaqAnchors";
import { ContentWrapper } from "../components/ContentPagesGeneralStyling";
import AccordionComponent from "../components/AccordionComponent";
import IconOne from "../assets/icons/icon_1_noBorder.svg";
import IconTwo from "../assets/icons/icon_2_noBorder.svg";
import IconThree from "../assets/icons/icon_3_noBorder.svg";
import IconFour from "../assets/icons/icon_4_noBorder.svg";
import CallToActionBox from "../components/CallToActionBox";

const Icon = styled.img`
  height: 21px;
  width: 21px;
  margin-right: var(--spacing-02);
`;

const TableOfContents = styled.div`
  margin-top: var(--spacing-09);
  display: flex;
  flex-direction: column;
`;

const Row = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-02);
`;

export default function HelpAreaPage({ plausibleDomain }) {
  const { t } = useTranslation();
  const mailto = t("helpAreaPage.mailto");
  const plausiblePropsContactUsButton = {
    method: "Hilfebereich / Schreiben Sie uns",
  };
  return (
    <>
      <ContentWrapper>
        <FormHeader title={t("helpAreaPage.formHeaderTitle")} />
        <TableOfContents>
          <Row>
            <Icon src={IconOne} alt="test" />
            <a href="#accordionCanIUseSection">
              {t("helpAreaPage.listOfContents.one")}
            </a>
          </Row>
          <Row>
            <Icon src={IconTwo} alt="test" />
            <a href="#letterActivationCodeSection">
              {t("helpAreaPage.listOfContents.two")}
            </a>
          </Row>
          <Row>
            <Icon src={IconThree} alt="test" />
            <a href="#submitTaxReturnSection">
              {t("helpAreaPage.listOfContents.three")}
            </a>
          </Row>
          <Row>
            <Icon src={IconFour} alt="test" />
            <a href="#afterSubmissionSection">
              {t("helpAreaPage.listOfContents.four")}
            </a>
          </Row>
        </TableOfContents>
        <AccordionComponent
          title={t("helpAreaPage.accordionCanIUseSection.heading")}
          items={accordionCanIUseSection}
          variant="marginTop"
          id="accordionCanIUseSection"
          plausibleDomain={plausibleDomain}
        />
        <AccordionComponent
          title={t("helpAreaPage.letterActivationCodeSection.heading")}
          items={letterActivationCodeSection}
          variant="marginTop"
          id="letterActivationCodeSection"
          plausibleDomain={plausibleDomain}
        />
        <AccordionComponent
          title={t("helpAreaPage.submitTaxReturnSection.heading")}
          items={submitTaxReturnSection}
          variant="marginTop"
          id="submitTaxReturnSection"
          plausibleDomain={plausibleDomain}
        />
        <AccordionComponent
          title={t("helpAreaPage.afterSubmissionSection.heading")}
          items={afterSubmissionSection}
          variant="marginTop"
          id="afterSubmissionSection"
          plausibleDomain={plausibleDomain}
        />
      </ContentWrapper>
      <CallToActionBox
        headline={t("helpAreaPage.questionInfoBox.heading")}
        anchor={mailto}
        plausibleGoal={t("helpAreaPage.questionInfoBox.plausibleGoal")}
        plausibleDomain={plausibleDomain}
        plausibleProps={plausiblePropsContactUsButton}
        buttonText={t("helpAreaPage.questionInfoBox.button")}
      />
    </>
  );
}

HelpAreaPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

HelpAreaPage.defaultProps = {
  plausibleDomain: undefined,
};
