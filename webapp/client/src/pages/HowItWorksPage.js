import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { Trans, useTranslation } from "react-i18next";
import {
  ContentWrapper,
  Headline2,
} from "../components/ContentPagesGeneralStyling";
import FormHeader from "../components/FormHeader";
import retirementDates from "../lib/retirementDate";
import HowItWorksComponent from "../components/HowItWorksComponent";
import ButtonAnchor from "../components/ButtonAnchor";
import OneIcon from "../assets/icons/Icon-1.svg";
import TwoIcon from "../assets/icons/Icon-2.svg";
import ThreeIcon from "../assets/icons/Icon-3.svg";
import FourIcon from "../assets/icons/Icon-4.svg";
import FiveIcon from "../assets/icons/Icon-5.svg";
import SixIcon from "../assets/icons/Icon-6.svg";
import SevenIcon from "../assets/icons/Icon-7.svg";
import CallToActionBox from "../components/CallToActionBox";

const VideoSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: var(--beige-300);
  padding: 48px 0 50px 0;

  @media (max-width: 768px) {
    padding: 48px 16px 50px 16px;
  }
`;

const HowItWorksVideoContainer = styled.div`
  position: relative;
  box-shadow: 20px 20px 50px rgba(0, 0, 0, 0.35);
  display: flex;
  max-width: 650px;

  @media (max-width: 768px) {
    max-width: 60%;
  }

  @media (max-width: 575px) {
    max-width: 100%;
  }
`;

const HowItWorksImage = styled.img`
  width: 100%;
  height: auto;
`;

const Div = styled.div`
  display: flex;
  justify-content: center;
  visibility: hidden;

  @media (max-width: 1279px) {
    visibility: visible;
  }
`;

export default function HowItWorksPage({ plausibleDomain }) {
  const { t } = useTranslation();

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          vorbereitenLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/vorbereiten" rel="noreferrer" target="_blank" />
          ),
        }}
      />
    );
  }

  const StepOne = {
    icon: {
      iconSrc: OneIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepOne.heading"),
    image: {
      src: "../../images/step1.png",
      alt: t("howItWorksPage.stepOne.imageAltText"),
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepTwo = {
    icon: {
      iconSrc: TwoIcon,
      altText: t("register.icons.iconTwo.altText"),
    },
    heading: t("howItWorksPage.stepTwo.heading"),
    text: "Wenn Sie die Steuererklärung gemeinsam als Paar machen möchten, reicht es aus, wenn sich eine Person registriert.",
    image: {
      src: "../../images/step2.png",
      alt: t("howItWorksPage.stepTwo.imageAltText"),
      srcSetDesktop: "../../images/step2.png",
      srcSetMobile: "../../images/step2_mobile.png",
    },
  };
  const StepThree = {
    icon: {
      iconSrc: ThreeIcon,
      altText: t("register.icons.iconThree.altText"),
    },
    heading: t("howItWorksPage.stepThree.heading"),
    image: {
      src: "../../images/step3.png",
      alt: t("howItWorksPage.stepThree.imageAltText"),
      srcSetDesktop: "../../images/step3.png",
      srcSetMobile: "../../images/step3_mobile.png",
    },
  };
  const StepFour = {
    icon: {
      iconSrc: FourIcon,
      altText: t("howItWorksPage.stepFour.iconaltText"),
    },
    heading: t("howItWorksPage.stepFour.heading"),
    text: "Ihr Freischaltcode ist 90 Tage nach der Registrierung für die erste Anmeldung gültig. Das Ablaudatum finden Sie auch auf Ihrem Brief unter „Gültigkeit(Ende)”.",
    image: {
      src: "../../images/step4.png",
      alt: t("howItWorksPage.stepFour.imageAltText"),
      srcSetDesktop: "../../images/step4.png",
      srcSetMobile: "../../images/step4.png",
    },
  };
  const StepFive = {
    icon: {
      iconSrc: FiveIcon,
      altText: t("howItWorksPage.stepFive.iconaltText"),
    },
    heading: t("howItWorksPage.stepFive.heading"),
    text: "Nach der ersten Anmeldung mit Ihrem Freischaltcode haben Sie 60 Tage Zeit, Ihre Steuererklärung auszufüllen und abzuschicken.",
    image: {
      src: "../../images/step5.png",
      alt: t("howItWorksPage.stepFive.imageAltText"),
      srcSetDesktop: "../../images/step5.png",
      srcSetMobile: "../../images/step5_mobile.png",
    },
  };
  const StepSix = {
    icon: {
      iconSrc: SixIcon,
      altText: t("howItWorksPage.stepSix.iconaltText"),
    },
    heading: t("howItWorksPage.stepSix.heading"),
    image: {
      src: "../../images/step6.png",
      alt: t("howItWorksPage.stepSix.imageAltText"),
      srcSetDesktop: "../../images/step6.png",
      srcSetMobile: "../../images/step6_mobile.png",
    },
  };
  const StepSeven = {
    icon: {
      iconSrc: SevenIcon,
      altText: t("howItWorksPage.stepSeven.iconaltText"),
    },
    heading: t("howItWorksPage.stepSeven.heading"),
    image: {
      src: "../../images/step7.png",
      alt: t("howItWorksPage.stepSeven.imageAltText"),
      srcSetDesktop: "../../images/step7.png",
      srcSetMobile: "../../images/step7_mobile.png",
    },
  };

  const newLocal = "https://www.youtube.com/watch?v=vP--fwSWtLE";
  const plausiblePropsPlayVideoButton = {
    props: {
      method: "Sofunktionierts / Erklärvideo",
    },
  };
  const plausiblePropsEligibilityStartButton = {
    props: {
      method: "Sofunktionierts / CTA Jetzt starten",
    },
  };
  const plausiblePropsHelpPageButton = {
    props: {
      method: "Sofunktionierts / Zum Hilfebereich",
    },
  };
  const startButton = {
    url: "/eligibility/step/welcome?link_overview=False",
    plausibleGoal: t("howItWorksPage.startButton.plausibleGoal"),
    plausibleProps: { plausiblePropsEligibilityStartButton },
  };

  const introText = (
    <>
      <p>{t("howItWorksPage.formHeaderTextOne")}</p>
      <p>{trans("howItWorksPage.formHeaderTextTwo")}</p>
    </>
  );
  return (
    <>
      <ContentWrapper marginBottom>
        <FormHeader
          title={t("howItWorksPage.formHeaderTitle")}
          intro={introText}
        />
      </ContentWrapper>
      <VideoSection>
        <Headline2 paddingVariant marginVariant>
          {t("howItWorksPage.stepsVideoSection.heading")}
        </Headline2>
        <HowItWorksVideoContainer>
          <HowItWorksImage
            src="/images/videoHowItWorks.png"
            alt={t("howItWorksPage.stepsVideoSection.imageAltText")}
          />
          <ButtonAnchor
            text={t("howItWorksPage.stepsVideoSection.buttonText")}
            url={newLocal}
            isExternalLink
            plausibleGoal={t("howItWorksPage.stepsVideoSection.plausibleGoal")}
            plausibleDomain={plausibleDomain}
            plausibleProps={plausiblePropsPlayVideoButton}
          />
        </HowItWorksVideoContainer>
      </VideoSection>
      <ContentWrapper
        marginLeftVariant
        marginVariant
        style={{
          display: "flex",
          flexDirection: "column",
        }}
      >
        <HowItWorksComponent
          heading={StepOne.heading}
          icon={StepOne.icon}
          image={StepOne.image}
          deadline={retirementDates.dateOne}
        />
        <HowItWorksComponent
          heading={StepTwo.heading}
          text={StepTwo.text}
          icon={StepTwo.icon}
          image={StepTwo.image}
          deadline={retirementDates.dateOne}
        />
        <HowItWorksComponent
          heading={StepThree.heading}
          text={StepThree.text}
          icon={StepThree.icon}
          image={StepThree.image}
        />
        <HowItWorksComponent
          heading={StepFour.heading}
          text={StepFour.text}
          icon={StepFour.icon}
          image={StepFour.image}
        />
        <HowItWorksComponent
          heading={StepFive.heading}
          text={StepFive.text}
          icon={StepFive.icon}
          image={StepFive.image}
          deadline={retirementDates.dateTwo}
        />
        <HowItWorksComponent
          heading={StepSix.heading}
          text={StepSix.text}
          icon={StepSix.icon}
          image={StepSix.image}
          deadline={retirementDates.dateTwo}
        />
        <HowItWorksComponent
          heading={StepSeven.heading}
          text={StepSeven.text}
          icon={StepSeven.icon}
          image={StepSeven.image}
          variant
          button={startButton}
          deadline={retirementDates.dateTwo}
        />
        <Div>
          <ButtonAnchor
            url="/eligibility/step/welcome?link_overview=False"
            plausibleGoal={t("howItWorksPage.startButton.plausibleGoal")}
            plausibleProps={plausiblePropsEligibilityStartButton}
            plausibleDomain={plausibleDomain}
            disabled
          >
            {t("howItWorksPage.startButton.text")}
          </ButtonAnchor>
        </Div>
      </ContentWrapper>
      <CallToActionBox
        headline={t("howItWorksPage.questionInfoBox.heading")}
        variant="outline"
        anchor="/hilfebereich"
        plausibleGoal={t("howItWorksPage.questionInfoBox.plausibleGoal")}
        plausibleProps={plausiblePropsHelpPageButton}
        plausibleDomain={plausibleDomain}
        buttonText={t("howItWorksPage.questionInfoBox.button")}
      />
    </>
  );
}

HowItWorksPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

HowItWorksPage.defaultProps = {
  plausibleDomain: undefined,
};
