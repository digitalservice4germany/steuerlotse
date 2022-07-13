import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import faqAnchorList from "../lib/faqAnchors";
import {
  ContentWrapper,
  Headline2,
} from "../components/ContentPagesGeneralStyling";
import AccordionComponent from "../components/AccordionComponent";
import ButtonAnchor from "../components/ButtonAnchor";

const Box = styled.div`
  padding: 60px 0px 90px 0px;
  background-color: var(--beige-200);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-height: 274px;
`;

export default function HelpAreaPage({ plausibleDomain }) {
  const { t } = useTranslation();

  return (
    <>
      <ContentWrapper>
        <FormHeader title={t("helpAreaPage.formHeaderTitle")} />
        <AccordionComponent
          title={t("LandingPage.Accordion.heading")}
          items={faqAnchorList}
          variant="marginTop"
        />
        <AccordionComponent
          title={t("LandingPage.Accordion.heading")}
          items={faqAnchorList}
          variant="marginTop"
        />
        <AccordionComponent
          title={t("LandingPage.Accordion.heading")}
          items={faqAnchorList}
          variant="marginTop"
        />
        <AccordionComponent
          title={t("LandingPage.Accordion.heading")}
          items={faqAnchorList}
          variant="marginTop"
        />
      </ContentWrapper>
      <Box style={{ marginTop: "5rem" }}>
        <Headline2 marginVariant paddingVariant>
          {t("howItWorksPage.questionInfoBox.heading")}
        </Headline2>
        <ButtonAnchor
          variant="outline"
          url="/hilfebereich"
          plausibleGoal={t("howItWorksPage.questionInfoBox.plausibleGoal")}
          plausibleDomain={plausibleDomain}
        >
          {t("howItWorksPage.questionInfoBox.button")}
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
