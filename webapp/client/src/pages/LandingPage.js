import React from "react";
import { t } from "i18next";
import PropTypes from "prop-types";
import styled from "styled-components";
import CardsComponent from "../components/CardsComponent";
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
  margin-top: 5rem;
  margin-bottom: var(--spacing-08);
  width: 50%;
  padding-right: 4%;

  @media (max-width: 1023px) {
    width: 100%;
    margin-top: var(--spacing-08);
    margin-bottom: 0;

    p:first-of-type {
      margin-top: 3rem !important;
    }
  }

  @media (max-width: 499px) {
    width: 100%;
    margin-top: var(--spacing-10);
  }

  & h1 {
    font-size: var(--text-3xl);
  }

  & p:first-of-type {
    margin-top: var(--spacing-07);
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

const cardsInfo = [
  {
    header: t("LandingPage.Cards.cardOne.header"),
    url: t("LandingPage.Cards.cardOne.url"),
  },
  {
    header: t("LandingPage.Cards.cardTwo.header"),
    url: t("LandingPage.Cards.cardTwo.url"),
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
        </LandingPageHeroContentWrapper>
      </LandingPageHeroWrapper>
      <CardsComponent cards={cardsInfo} />
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
    </div>
  );
}

LandingPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

LandingPage.defaultProps = {
  plausibleDomain: undefined,
};
