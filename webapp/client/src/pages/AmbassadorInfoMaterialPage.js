import React from "react";
import styled from "styled-components";
// import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";

const HeadingText = styled.div`
font-size=var(--text-4xl)
`;
const SubHeadingText = styled.div``;
const ParagraphHeading = styled.div``;
const ContentText = styled.div``;

export default function AmbassadorInfoMaterialPage() {
  const { t } = useTranslation();
  return (
    <div>
      <HeadingText>{t("AmbassadorMaterial.Heading")}</HeadingText>
      <SubHeadingText>{t("AmbassadorMaterial.SubHeading")}</SubHeadingText>
      <img src="/images/hero-image-botschafter.png" alt="Botschafter" />
      <ParagraphHeading>
        {t("AmbassadorMaterial.Paragraph.DownloadInformationText")}
      </ParagraphHeading>
      <ContentText>
        {t("AmbassadorMaterial.Paragraph.InfoBroshureDownloadLink")}
      </ContentText>
      <ContentText>
        {t("AmbassadorMaterial.Paragraph.SteuerlotsenFlyerLink")}
      </ContentText>

      <ParagraphHeading>
        {t("AmbassadorMaterial.Paragraph.HowItWorks")}
      </ParagraphHeading>
      <ContentText>
        {t("AmbassadorMaterial.Paragraph.DownloadInformationText")}
      </ContentText>
      <ParagraphHeading>
        {t("AmbassadorMaterial.Paragraph.Heading")}
      </ParagraphHeading>
      <ContentText>{t("AmbassadorMaterial.Paragraph.Text")}</ContentText>
    </div>
  );
}

AmbassadorInfoMaterialPage.propTypes = {};

AmbassadorInfoMaterialPage.defaultProps = {};
