import React from "react";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import { ContentWrapper } from "../components/ContentPagesGeneralStyling";
import FormHeader from "../components/FormHeader";
import SecondaryAnchorButton from "../components/SecondaryAnchorButton";
import HowItWorksComponent from "../components/HowItWorksComponent";
import InfoBoxGrundsteuer from "../components/InfoBoxGrundsteuer";
import ButtonAnchor from "../components/ButtonAnchor";

const VideoSection = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: var(--beige-300);
  padding: 48px 50px;
`;

const HowItWorksVideoContainer = styled.div`
  position: relative;
  max-width: 930px;
  width: 75vw;

  @media (max-width: 1024px) {
    width: 85vw;
  }

  @media (max-width: 425px) {
    width: 90vw;
  }
`;

const HowItWorksImage = styled.img`
  width: 100%;
  height: auto;
`;

export default function HowItWorksPage() {
  const { t } = useTranslation();

  return (
    <>
      <ContentWrapper>
        <FormHeader
          title={t("vorbereitenOverview.Paragraph1.heading")}
          intro={t("vorbereitenOverview.Paragraph1.text")}
        />
      </ContentWrapper>
      <VideoSection>
        <h2>Schritt-für-Schritt Anleitung (Erklärvideo)</h2>
        <HowItWorksVideoContainer>
          <HowItWorksImage
            src="/images/test.png"
            alt="Link to How It Works Video"
          />
          <SecondaryAnchorButton
            text="Auf Youtube abspielen"
            url="https://www.youtube.com/watch?v=vP--fwSWtLE"
            className="outline-0"
            isExternalLink
            plausibleName="Youtube-Link clicked"
          />
        </HowItWorksVideoContainer>
      </VideoSection>
      <ContentWrapper marginVariant>
        <HowItWorksComponent />
        <HowItWorksComponent />
        <HowItWorksComponent borderVariant />
      </ContentWrapper>
      <ButtonAnchor />
      <InfoBoxGrundsteuer />
    </>
  );
}
