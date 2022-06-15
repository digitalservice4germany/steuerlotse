import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation, Trans } from "react-i18next";
import ButtonAnchor from "../components/ButtonAnchor";
import { HeroImage, TextContent } from "../components/ContentPageStyles";

import {
  Headline1,
  Headline2,
  ParagraphLarge,
  ContentWrapper,
} from "../components/ContentPagesGeneralStyling";

const Headline1Ambassador = styled(Headline1)`
  margin-top: var(--spacing-11);

  @media (max-width: 1024px) {
    margin-top: var(--spacing-05);
  }
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
    <ContentWrapper>
      <Headline1Ambassador>
        {t("AmbassadorMaterial.Heading")}
      </Headline1Ambassador>
      <ParagraphLarge>{t("AmbassadorMaterial.SubHeading")}</ParagraphLarge>
      <HeroImage
        src="/images/hero-image-botschafter.png"
        alt="Bilder von Rentnerinnen und Rentnern beim Ausfüllen ihrer digitalen Steuererklärung"
      />
      <Headline2Ambassador>
        {t("AmbassadorMaterial.Section.whatSteuerlotseDoes.heading")}
      </Headline2Ambassador>
      <TextContent>
        {t("AmbassadorMaterial.Section.whatSteuerlotseDoes.text")}
      </TextContent>

      <Headline2Ambassador>
        {t("AmbassadorMaterial.Section.downloadInformation.heading")}
      </Headline2Ambassador>
      <TextContent>
        {t("AmbassadorMaterial.Section.downloadInformation.text")}
      </TextContent>

      <div>
        <ButtonAnchor
          url="/download_informationsbroschure_pdf"
          plausibleDomain={plausibleDomain}
          plausibleName="Download Informationsbroschüre"
          className="mb-3"
        >
          {t(
            "AmbassadorMaterial.Section.downloadInformation.informationButtonText"
          )}
        </ButtonAnchor>
      </div>
      <div>
        <ButtonAnchor
          url="/download_steuerlotsen_flyer.pdf"
          plausibleDomain={plausibleDomain}
          plausibleName="Download Steuerlotsen-Flyer"
          className="mb-3"
        >
          {t("AmbassadorMaterial.Section.downloadInformation.flyerButtonText")}
        </ButtonAnchor>
      </div>

      <Headline2Ambassador>
        {t("AmbassadorMaterial.Section.freeInformation.heading")}
      </Headline2Ambassador>
      <TextContent>
        {trans("AmbassadorMaterial.Section.freeInformation.text")}
      </TextContent>
      <ButtonAnchor
        url="mailto:kontakt@steuerlotse-rente.de\"
        plausibleDomain={plausibleDomain}
        plausibleName="Download Informationsbroschüre"
        className="mb-3"
      >
        {t("AmbassadorMaterial.Section.freeInformation.buttonText")}
      </ButtonAnchor>

      <Headline2Ambassador>
        {t("AmbassadorMaterial.Section.contactUs.heading")}
      </Headline2Ambassador>
      <TextContent>
        {t("AmbassadorMaterial.Section.contactUs.text")}
      </TextContent>
    </ContentWrapper>
  );
}

AmbassadorInfoMaterialPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

AmbassadorInfoMaterialPage.defaultProps = { plausibleDomain: undefined };
