import React from "react";
import { useTranslation } from "react-i18next";
import InfoBox from "../components/InfoBox";
import StepHeaderButtons from "../components/StepHeaderButtons";
// eslint-disable-next-line import/named
import { anchorBack, anchorList } from "../lib/contentPagesAnchors";
import {
  ContentWrapper,
  List,
  AnchorListItem,
  Headline1,
  Headline2,
  Paragraph,
  ParagraphLarge,
} from "../components/ContentPagesGeneralStyling";

export default function ReplacementCostsInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Sonstige außergewöhnliche Belastungen")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <Headline1>{t("ReplacementCostsInfo.Section1.Heading")}</Headline1>
        <ParagraphLarge>
          {t("ReplacementCostsInfo.Section1.Text")}
        </ParagraphLarge>
        <Headline2>{t("ReplacementCostsInfo.Section2.Heading")}</Headline2>
        <Paragraph>{t("ReplacementCostsInfo.Section2.Text")}</Paragraph>
        <Paragraph>{t("ReplacementCostsInfo.Section2.Text2")}</Paragraph>

        <Headline2>{t("ReplacementCostsInfo.Section3.Heading")}</Headline2>
        <Paragraph>{t("ReplacementCostsInfo.Section3.Text")}</Paragraph>
        <Paragraph>{t("ReplacementCostsInfo.Section3.Text2")}</Paragraph>

        <Headline2>{t("ReplacementCostsInfo.Section4.Heading")}</Headline2>
        <List aria-label="anchor-list">{anchorListItemsMap}</List>
      </ContentWrapper>
      <InfoBox />
    </>
  );
}
