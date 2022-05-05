import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation, Trans } from "react-i18next";
import { HeroImage, TextContent } from "../components/ContentPageStyles";
import DownloadLink from "../components/DownloadLink";
import SecondaryAnchorButton from "../components/SecondaryAnchorButton";
import {
  Headline1,
  Headline2,
  ParagraphLarge,
} from "../components/ContentPagesGeneralStyling";

const HowItWorksVideoContainer = styled.div`
  position: relative;
`;

const HowItWorksImage = styled.img`
  max-width: 100%;
  height: auto;
`;

const Headline1Ambassador = styled(Headline1)`
  margin-top: var(--spacing-11);

  @media (max-width: 1024px) {
    margin-top: var(--spacing-05);
  }
`;

const DownloadLinkStyled = styled(DownloadLink)`
  display: block;
`;

const Headline2Ambassador = styled(Headline2)`
  margin-bottom: var(--spacing-04);

  @media (min-width: 768px) {
    font-size: var(--text-xxl);
  }
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
    <>
      <Headline1Ambassador>
        {t("AmbassadorMaterial.Heading")}
      </Headline1Ambassador>
      <ParagraphLarge>{t("AmbassadorMaterial.SubHeading")}</ParagraphLarge>
      <HeroImage
        src="/images/hero-image-botschafter.png"
        alt="Bilder von Rentnerinnen und Rentnern beim Ausfüllen ihrer digitalen Steuererklärung"
      />
      <Headline2Ambassador>
        {t("AmbassadorMaterial.Paragraph.DownloadInformationText")}
      </Headline2Ambassador>
      <DownloadLinkStyled
        text={t("AmbassadorMaterial.Paragraph.InfoBroschureDownloadLink")}
        url="/download_informationsbroschure_pdf"
        plausibleDomain={plausibleDomain}
        plausibleName="Download Informationsbroschüre"
        className="mb-3"
      />
      <DownloadLinkStyled
        text={t("AmbassadorMaterial.Paragraph.SteuerlotsenFlyerLink")}
        url="/download_steuerlotsen_flyer.pdf"
        plausibleDomain={plausibleDomain}
        plausibleName="Download Steuerlotsen-Flyer"
      />
      <Headline2Ambassador>
        {t("AmbassadorMaterial.Paragraph.FreeFlyerHeading")}
      </Headline2Ambassador>
      <TextContent>
        {trans("AmbassadorMaterial.Paragraph.FreeFlyerText")}
      </TextContent>
      <Headline2Ambassador>
        {t("AmbassadorMaterial.Paragraph.HowItWorks")}
      </Headline2Ambassador>
      <HowItWorksVideoContainer>
        <HowItWorksImage
          src="/images/How_It_Works_Video.png"
          alt="Erklärvideo auf Youtube abspielen"
        />
        <SecondaryAnchorButton
          text="Auf Youtube abspielen"
          url="https://www.youtube.com/watch?v=vP--fwSWtLE"
          className="outline-0"
          isExternalLink
          plausibleDomain={plausibleDomain}
          plausibleName="Youtube-Link clicked"
        />
      </HowItWorksVideoContainer>
      <Headline2Ambassador>
        {t("AmbassadorMaterial.Paragraph.AnyOtherQuestions")}
      </Headline2Ambassador>
      <TextContent>
        {trans("AmbassadorMaterial.Paragraph.ContactUs")}
      </TextContent>
    </>
  );
}

AmbassadorInfoMaterialPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

AmbassadorInfoMaterialPage.defaultProps = { plausibleDomain: undefined };
