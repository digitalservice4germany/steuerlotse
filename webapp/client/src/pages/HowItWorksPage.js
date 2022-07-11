import React from "react";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import {
  ContentWrapper,
  Headline2,
} from "../components/ContentPagesGeneralStyling";
import FormHeader from "../components/FormHeader";
import SecondaryAnchorButton from "../components/SecondaryAnchorButton";
import HowItWorksComponent from "../components/HowItWorksComponent";
import InfoBoxGrundsteuer from "../components/InfoBoxGrundsteuer";
import ButtonAnchor from "../components/ButtonAnchor";
import OneIcon from "../assets/icons/Icon-1.svg";
import TwoIcon from "../assets/icons/Icon-2.svg";
import ThreeIcon from "../assets/icons/Icon-3.svg";
import FourIcon from "../assets/icons/Icon-4.svg";
import FiveIcon from "../assets/icons/Icon-5.svg";
import SixIcon from "../assets/icons/Icon-6.svg";
import SevenIcon from "../assets/icons/Icon-7.svg";

const VideoSection = styled.div`
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  background-color: var(--beige-300);
  padding: 48px 0 70px 250px;
`;

const HowItWorksVideoContainer = styled.div`
  position: relative;
  box-shadow: 20px 20px 50px rgba(0, 0, 0, 0.35);
  display: flex;
  /* justify-content: center; */
  /* max-width: 650px; */
  width: 65%;
  /* margin-top: var(--spacing-03); */
`;

const HowItWorksImage = styled.img`
  width: 100%;
  height: auto;
`;

export default function HowItWorksPage() {
  const { t } = useTranslation();

  const StepOne = {
    icon: {
      iconSrc: OneIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepOne.heading"),
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepTwo = {
    icon: {
      iconSrc: TwoIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepTwo.heading"),
    text: "Wenn Sie die Steuererklärung gemeinsam als Paar machen möchten, reicht es aus, wenn sich eine Person registriert.",
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepThree = {
    icon: {
      iconSrc: ThreeIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepThree.heading"),
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepFour = {
    icon: {
      iconSrc: FourIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepFour.heading"),
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepFive = {
    icon: {
      iconSrc: FiveIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepFive.heading"),
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepSix = {
    icon: {
      iconSrc: SixIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepSix.heading"),
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };
  const StepSeven = {
    icon: {
      iconSrc: SevenIcon,
      altText: t("register.icons.iconOne.altText"),
    },
    heading: t("howItWorksPage.stepSeven.heading"),
    image: {
      src: "../../images/step1.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
      srcSetDesktop: "../../images/step1.png",
      srcSetMobile: "../../images/step1_mobile.png",
    },
  };

  return (
    <>
      <ContentWrapper>
        <FormHeader
          title={t("howItWorksPage.formHeaderTitle")}
          intro={t("howItWorksPage.formHeaderText")}
        />
      </ContentWrapper>
      <VideoSection>
        <Headline2 paddingVariant marginVariant>
          {t("howItWorksPage.stepsVideoSection.heading")}
        </Headline2>
        <HowItWorksVideoContainer>
          <HowItWorksImage
            src="/images/test.png"
            alt={t("howItWorksPage.stepsVideoSection.imageAltText")}
          />
          <SecondaryAnchorButton
            text="Auf Youtube abspielen"
            url="https://www.youtube.com/watch?v=vP--fwSWtLE"
            className="outline-0"
            isExternalLink
            plausibleName="Erklärvideo"
          />
        </HowItWorksVideoContainer>
      </VideoSection>
      <ContentWrapper marginVariant>
        <HowItWorksComponent
          heading={StepOne.heading}
          icon={StepOne.icon}
          image={StepOne.image}
        />
        <HowItWorksComponent
          heading={StepTwo.heading}
          text={StepTwo.text}
          icon={StepTwo.icon}
          image={StepTwo.image}
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
        />
        <HowItWorksComponent
          heading={StepSix.heading}
          text={StepSix.text}
          icon={StepSix.icon}
          image={StepSix.image}
        />
        <HowItWorksComponent
          heading={StepSeven.heading}
          text={StepSeven.text}
          icon={StepSeven.icon}
          image={StepSeven.image}
          borderVariant
        />
      </ContentWrapper>
      <ButtonAnchor />
      <InfoBoxGrundsteuer />
    </>
  );
}
