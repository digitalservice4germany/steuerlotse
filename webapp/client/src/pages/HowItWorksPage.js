import React from "react";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import { ContentWrapper } from "../components/ContentPagesGeneralStyling";
import FormHeader from "../components/FormHeader";

const Figure = styled.figure`
  margin: 0;
  align-self: end;
  width: 100%;
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }

  @media (max-width: 767px) {
    align-self: center;
  }
`;

const VideoSection = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 48px 0px 48px 144px;
  background-color: var(--beige-300);
`;

export default function HowItWorksPage() {
  const { t } = useTranslation();

  return (
    <ContentWrapper>
      <FormHeader
        title={t("vorbereitenOverview.Paragraph1.heading")}
        intro={t("vorbereitenOverview.Paragraph1.text")}
      />
      <VideoSection>
        <h2>Schritt-für-Schritt Anleitung (Erklärvideo)</h2>
        <Figure>
          <picture>
            <img
              src="../images/hero_info_tax_return_pensioners.png"
              alt="Tablets mit Webapp des Steuerlotsen"
            />
          </picture>
        </Figure>
      </VideoSection>
    </ContentWrapper>
  );
}
