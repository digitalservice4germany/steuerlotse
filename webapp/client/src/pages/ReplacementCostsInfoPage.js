import React from "react";
import { useTranslation } from "react-i18next";
import InfoBox from "../components/InfoBox";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormHeader from "../components/FormHeader";
// eslint-disable-next-line import/named
import {
  anchorBack,
  anchorList,
  anchorRegister,
} from "../lib/contentPagesAnchors";
import {
  ContentWrapper,
  List,
  AnchorListItem,
  Headline2,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function ReplacementCostsInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Wiederbeschaffungskosten")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <FormHeader
          title={t("ReplacementCostsInfo.Section1.Heading")}
          intro={t("ReplacementCostsInfo.Section1.Text")}
        />
        <Headline2>{t("ReplacementCostsInfo.Section2.Heading")}</Headline2>
        <Paragraph>{t("ReplacementCostsInfo.Section2.Text")}</Paragraph>
        <Paragraph>{t("ReplacementCostsInfo.Section2.Text2")}</Paragraph>

        <Headline2>{t("ReplacementCostsInfo.Section3.Heading")}</Headline2>
        <Paragraph>{t("ReplacementCostsInfo.Section3.Text")}</Paragraph>
        <Paragraph>{t("ReplacementCostsInfo.Section3.Text2")}</Paragraph>

        <Headline2>{t("ReplacementCostsInfo.Section4.Heading")}</Headline2>
        <List aria-label="anchor-list">{anchorListItemsMap}</List>
      </ContentWrapper>
      <InfoBox
        boxHeadline={anchorRegister.headline}
        boxText={t("InfoBox.text")}
        anchor={anchorRegister}
      />
    </>
  );
}
