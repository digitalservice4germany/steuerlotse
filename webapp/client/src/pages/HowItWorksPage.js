import React from "react";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import {
  ContentWrapper,
  Headline2,
} from "../components/ContentPagesGeneralStyling";
import FormHeader from "../components/FormHeader";
import HowItWorksComponent from "../components/HowItWorksComponent";
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

const Box = styled.div`
  padding: 60px 0px 90px 0px;
  background-color: var(--beige-200);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-height: 274px;
`;

const Div = styled.div`
  display: flex;
  justify-content: center;
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
      alt: "",
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
      alt: "",
      srcSetDesktop: "../../images/step2.png",
      srcSetMobile: "../../images/step2_mobile.png",
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
      alt: "",
      srcSetDesktop: "../../images/step3.png",
      srcSetMobile: "../../images/step3_mobile.png",
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
      alt: "",
      srcSetDesktop: "../../images/step4.png",
      srcSetMobile: "../../images/step4.png",
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
      alt: "",
      srcSetDesktop: "../../images/step5.png",
      srcSetMobile: "../../images/step5_mobile.png",
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
      alt: "",
      srcSetDesktop: "../../images/step6.png",
      srcSetMobile: "../../images/step6_mobile.png",
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
      alt: "",
      srcSetDesktop: "../../images/step7.png",
      srcSetMobile: "../../images/step7_mobile.png",
    },
  };

  const newLocal = "https://www.youtube.com/watch?v=vP--fwSWtLE";
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
          <ButtonAnchor
            text="Auf Youtube abspielen"
            url={newLocal}
            isExternalLink
            plausibleName="Erklärvideo"
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
          variant
        />
        <Div>
          <ButtonAnchor url="/eligibility/step/welcome?link_overview=False">
            {t("howItWorksPage.startButton")}
          </ButtonAnchor>
        </Div>
      </ContentWrapper>
      <Box>
        <Headline2 marginVariant paddingVariant>
          {t("howItWorksPage.questionInfoBox.heading")}
        </Headline2>
        <ButtonAnchor variant="outline" url="/">
          {t("howItWorksPage.questionInfoBox.button")}
        </ButtonAnchor>
      </Box>
    </>
  );
}
