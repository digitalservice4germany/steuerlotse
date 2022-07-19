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
import {
  ContentWrapper,
  Headline2,
} from "../components/ContentPagesGeneralStyling";
import AccordionComponent from "../components/AccordionComponent";
import ButtonAnchor from "../components/ButtonAnchor";
import IconOne from "../assets/icons/icon_1_noBorder.svg";
import IconTwo from "../assets/icons/icon_2_noBorder.svg";
import IconThree from "../assets/icons/icon_3_noBorder.svg";
import IconFour from "../assets/icons/icon_4_noBorder.svg";

const Box = styled.div`
  padding: 60px 0px 90px 0px;
  background-color: var(--beige-200);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-height: 274px;
`;

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
        />
        <AccordionComponent
          title={t("helpAreaPage.letterActivationCodeSection.heading")}
          items={letterActivationCodeSection}
          variant="marginTop"
          id="letterActivationCodeSection"
        />
        <AccordionComponent
          title={t("helpAreaPage.submitTaxReturnSection.heading")}
          items={submitTaxReturnSection}
          variant="marginTop"
          id="submitTaxReturnSection"
        />
        <AccordionComponent
          title={t("helpAreaPage.afterSubmissionSection.heading")}
          items={afterSubmissionSection}
          variant="marginTop"
          id="afterSubmissionSection"
        />
      </ContentWrapper>
      <Box style={{ marginTop: "5rem" }}>
        <Headline2 marginVariant paddingVariant>
          {t("helpAreaPage.questionInfoBox.heading")}
        </Headline2>
        <ButtonAnchor
          url={mailto}
          plausibleGoal={t("helpAreaPage.questionInfoBox.plausibleGoal")}
          plausibleDomain={plausibleDomain}
        >
          {t("helpAreaPage.questionInfoBox.button")}
        </ButtonAnchor>
      </Box>
    </>
  );
}

HelpAreaPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

HelpAreaPage.defaultProps = {
  plausibleDomain: undefined,
};
