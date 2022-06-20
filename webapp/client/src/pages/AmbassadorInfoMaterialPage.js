import React from "react";
import PropTypes from "prop-types";
import { useTranslation, Trans } from "react-i18next";
import FormHeader from "../components/FormHeader";
import ButtonAnchor from "../components/ButtonAnchor";
import { Picture } from "../components/ContentPageStyles";

import {
  Headline2,
  ContentWrapper,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

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
      <FormHeader
        title={t("AmbassadorMaterial.Heading")}
        intro={t("AmbassadorMaterial.SubHeading")}
      />
      <Picture marginTopVariant>
        <img
          src="/images/hero-image-botschafter.png"
          alt="Hybrid-Veranstaltung mit Personen im Raum und in einer Videokonferenz"
        />
      </Picture>
      <Headline2>
        {t("AmbassadorMaterial.Section.whatSteuerlotseDoes.heading")}
      </Headline2>
      <Paragraph>
        {t("AmbassadorMaterial.Section.whatSteuerlotseDoes.text")}
      </Paragraph>
      <Paragraph>
        {t("AmbassadorMaterial.Section.whatSteuerlotseDoes.text2")}
      </Paragraph>

      <Headline2>
        {t("AmbassadorMaterial.Section.downloadInformation.heading")}
      </Headline2>
      <Paragraph>
        {t("AmbassadorMaterial.Section.downloadInformation.text")}
      </Paragraph>
      <div>
        <ButtonAnchor
          url="/download_informationsbroschure_pdf"
          plausibleDomain={plausibleDomain}
          plausibleName="Download Informationsbroschüre"
          className="mb-3"
          marginTop
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
      <Headline2>
        {t("AmbassadorMaterial.Section.freeInformation.heading")}
      </Headline2>
      <Paragraph>
        {trans("AmbassadorMaterial.Section.freeInformation.text")}
      </Paragraph>
      <Paragraph>
        {trans("AmbassadorMaterial.Section.freeInformation.text2")}
      </Paragraph>
      <ButtonAnchor
        url="mailto:kontakt@steuerlotse-rente.de\"
        plausibleDomain={plausibleDomain}
        plausibleName="Download Informationsbroschüre"
        className="mb-3"
        marginTop
      >
        {t("AmbassadorMaterial.Section.freeInformation.buttonText")}
      </ButtonAnchor>
      <Headline2>{t("AmbassadorMaterial.Section.contactUs.heading")}</Headline2>
      <Paragraph>{t("AmbassadorMaterial.Section.contactUs.text")}</Paragraph>
    </ContentWrapper>
  );
}

AmbassadorInfoMaterialPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

AmbassadorInfoMaterialPage.defaultProps = { plausibleDomain: undefined };
