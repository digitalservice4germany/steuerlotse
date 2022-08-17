import React from "react";
import { t } from "i18next";
import PropTypes from "prop-types";
import styled from "styled-components";
import AccordionComponent from "../components/AccordionComponent";
import faqAnchorList from "../lib/faqAnchors";
import ButtonAnchor from "../components/ButtonAnchor";
import CardsComponent from "../components/CardsComponent";
import InfoBoxGrundsteuer from "../components/InfoBoxGrundsteuer";
import CallToActionBox from "../components/CallToActionBox";

const LandingPageHeroWrapper = styled.div`
  display: flex;
  padding-left: 2rem;

  @media (max-width: 1023px) {
    flex-direction: column;
  }

  @media (max-width: 768px) {
    padding-left: 1rem;
  }
`;

const LandingPageHeroContentWrapper = styled.div`
  margin-top: calc(var(--spacing-11) + 1.5rem);
  width: 50%;
  padding-right: 4%;

  @media (max-width: 1023px) {
    width: 100%;
    margin-top: var(--spacing-08);
  }

  @media (max-width: 499px) {
    width: 100%;
    margin-top: var(--spacing-10);
  }

  & h1 {
    font-size: var(--text-3xl);
  }

  & p:first-of-type {
    margin-top: 3rem;
  }

  & ul {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
  }

  & li {
    margin-top: 0.25rem;
  }

  & p:nth-of-type(2) {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-family: var(--font-bold);
  }
`;

const Figure = styled.div`
  width: 50%;

  & img {
    width: 95%;
    max-height: 650px;
    object-fit: contain;
  }

  @media (max-width: 1023px) {
    width: 100%;
    margin: var(--spacing-06) 0;
  }

  @media (max-width: 500px) {
    display: none;
  }
`;

const AccordionWrapper = styled.div`
  width: 60%;
  margin: var(--spacing-11) auto;

  & h2 {
    margin-bottom: var(--spacing-03);
    font-size: var(--text-3xl);
  }

  @media (max-width: 767px) {
    width: 100%;
    padding: 0 15px;
  }
`;

const cardsInfo = [
  {
    header: t("LandingPage.Cards.cardOne.header"),
    text: t("LandingPage.Cards.cardOne.text"),
    url: t("LandingPage.Cards.cardOne.url"),
  },
  {
    header: t("LandingPage.Cards.cardTwo.header"),
    text: t("LandingPage.Cards.cardTwo.text"),
    url: t("LandingPage.Cards.cardTwo.url"),
  },
  {
    header: t("LandingPage.Cards.cardThree.header"),
    text: t("LandingPage.Cards.cardThree.text"),
    url: t("LandingPage.Cards.cardThree.url"),
  },
];

export default function LandingPage({ plausibleDomain }) {
  const plausibleMethodStart = {
    method: "start",
  };

  return (
    <div>
      <LandingPageHeroWrapper>
        <LandingPageHeroContentWrapper>
          <h1>{t("LandingPage.Hero.title")}</h1>
          <p>{t("LandingPage.Hero.subTitle")}</p>
          <ul className="form-list">
            <li>{t("LandingPage.Hero.listItem1")}</li>
            <li>{t("LandingPage.Hero.listItem2")}</li>
            <li>{t("LandingPage.Hero.listItem3")}</li>
          </ul>
          <p>{t("LandingPage.Hero.eligibilityTest")}</p>
          <ButtonAnchor
            url="/eligibility/step/first_input_step"
            plausibleGoal={t("LandingPage.Hero.plausibleGoal")}
            plausibleDomain={plausibleDomain}
            marginVariant
          >
            {t("LandingPage.Hero.checkUseButton")}
          </ButtonAnchor>
        </LandingPageHeroContentWrapper>
        <Figure>
          <picture>
            <source
              media="(min-width: 1024px)"
              srcSet="../images/hero-image-big.png"
            />
            <source
              media="(min-width: 320px)"
              srcSet="../images/hero-image-small.png"
            />
            <img
              src="../images/hero-image-small.png"
              alt="Bilder von Rentnerinnen und Rentnern beim Ausfüllen ihrer digitalen Steuererklärung."
            />
          </picture>
        </Figure>
      </LandingPageHeroWrapper>
      <CardsComponent cards={cardsInfo} />
      <AccordionWrapper>
        <AccordionComponent
          title={t("LandingPage.Accordion.heading")}
          items={faqAnchorList}
          variant
        />
      </AccordionWrapper>
      <CallToActionBox
        colorVariant
        multipleButtons
        plausibleDomain={plausibleDomain}
        variant="outline"
        headline={t("helpAreaPage.questionInfoBox.heading")}
        firstButtonText={t("LandingPage.cta.howItWorksButtonText")}
        firstButtonUrl="/sofunktionierts"
        firstButtonPlausibleGoal="So funktionierts"
        firstButtonPlausibleProps={plausibleMethodStart}
        secondButtonText={t("howItWorksPage.questionInfoBox.button")}
        secondButtonUrl="/hilfebereich"
        secondButtonPlausibleGoal="zum Hilfebereich"
        secondButtonPlausibleProps={plausibleMethodStart}
      />
      <InfoBoxGrundsteuer />
    </div>
  );
}

LandingPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

LandingPage.defaultProps = {
  plausibleDomain: undefined,
};
