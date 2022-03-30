import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation, Trans } from "react-i18next";
import {
  TopSpacing,
  HeadingText,
  SectionIntro,
  SubHeadingText,
  HeroImage,
  ContentSection,
  TextContent,
  ParagraphHeading,
} from "../components/ContentPageStyles";
import DownloadLink from "../components/DownloadLink";
import SecondaryAnchorButton from "../components/SecondaryAnchorButton";

const HowItWorksVideoContainer = styled.div`
  position: relative;
  max-width: 930px;
  width: 930px;
`;

const HowItWorksImage = styled.img`
  width: 100%;
  height: auto;
`;

export default function AmbassadorInfoMaterialPage({ plausibleDomain }) {
  const { t } = useTranslation();
  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          mailToContact: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="mailto:kontakt@steuerlotse-rente.de\" />
          ),
        }}
      />
    );
  }
  return (
    <TopSpacing>
      <SectionIntro>
        <HeadingText className="font-weight-bold my-4 h1">
          {t("AmbassadorMaterial.Heading")}
        </HeadingText>
        <SubHeadingText>{t("AmbassadorMaterial.SubHeading")}</SubHeadingText>
      </SectionIntro>
      <HeroImage
        src="/images/hero-image-botschafter.png"
        alt="Bilder von Rentnerinnen und Rentnern beim Ausfüllen ihrer digitalen Steuererklärung"
      />
      <ContentSection>
        <ParagraphHeading className="h2 font-weight-bold my-3">
          {t("AmbassadorMaterial.Paragraph.DownloadInformationText")}
        </ParagraphHeading>
        <DownloadLink
          text={t("AmbassadorMaterial.Paragraph.InfoBroshureDownloadLink")}
          url="/download_pf/print.pdf"
          plausibleDomain={plausibleDomain}
          plausibleName="Download Informationsbroschüre"
          className="mb-3"
        />
        <DownloadLink
          text={t("AmbassadorMaterial.Paragraph.SteuerlotsenFlyerLink")}
          url="/download_pf/print.pdf"
          plausibleDomain={plausibleDomain}
          plausibleName="Download Steuerlotsen-Flyer"
        />
      </ContentSection>
      <ContentSection>
        <ParagraphHeading className="font-weight-bold">
          {t("AmbassadorMaterial.Paragraph.HowItWorks")}
        </ParagraphHeading>
        <HowItWorksVideoContainer>
          <HowItWorksImage
            src="/images/How_It_Works_Video.png"
            alt="Link to How It Works Video"
          />
          <SecondaryAnchorButton
            text="Auf Youtube abspielen"
            url="https://www.youtube.com/watch?v=vP--fwSWtLE"
            className="outline-0"
            isLinkingOutLink
            plausibleDomain={plausibleDomain}
            plausibleName="Youtube-Link clicked"
          />
        </HowItWorksVideoContainer>
      </ContentSection>
      <ContentSection>
        <ParagraphHeading className="font-weight-bold">
          {t("AmbassadorMaterial.Paragraph.AnyOtherQuestions")}
        </ParagraphHeading>
        <TextContent>
          {trans("AmbassadorMaterial.Paragraph.ContactUs")}
        </TextContent>
      </ContentSection>
    </TopSpacing>
  );
}

AmbassadorInfoMaterialPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

AmbassadorInfoMaterialPage.defaultProps = { plausibleDomain: undefined };
