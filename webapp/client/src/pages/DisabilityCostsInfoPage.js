import React from "react";
import { useTranslation } from "react-i18next";
import InfoBox from "../components/InfoBox";
import StepHeaderButtons from "../components/StepHeaderButtons";
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
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
  ParagraphLarge,
} from "../components/ContentPagesGeneralStyling";

export default function DisabilityCostsInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Angaben bei einer Behinderung")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  const listLumpSumInfo = [
    {
      text: t("DisabilityCostsInfo.Section3.ListItem1"),
    },
    {
      text: t("DisabilityCostsInfo.Section3.ListItem2"),
    },
    {
      text: t("DisabilityCostsInfo.Section3.ListItem3"),
    },
  ];

  const listDisabilityExpenses = [
    {
      text: t("DisabilityCostsInfo.Section4.ListItem1"),
    },
    {
      text: t("DisabilityCostsInfo.Section4.ListItem2"),
    },
    {
      text: t("DisabilityCostsInfo.Section4.ListItem3"),
    },
    {
      text: t("DisabilityCostsInfo.Section4.ListItem4"),
    },
  ];

  const listLumpSumInfoMap = listLumpSumInfo.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  const listDisabilityExpensesMap = listDisabilityExpenses.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />

        <Headline1>{t("DisabilityCostsInfo.Section1.Heading")}</Headline1>
        <ParagraphLarge>
          {t("DisabilityCostsInfo.Section1.Text")}
        </ParagraphLarge>

        <Headline2>{t("DisabilityCostsInfo.Section2.Heading")}</Headline2>
        <Paragraph>{t("DisabilityCostsInfo.Section2.Text")}</Paragraph>

        <Headline2>{t("DisabilityCostsInfo.Section3.Heading")}</Headline2>
        <Paragraph>{t("DisabilityCostsInfo.Section3.Text")}</Paragraph>
        <List aria-label="first-list">{listLumpSumInfoMap}</List>

        <Headline2>{t("DisabilityCostsInfo.Section4.Heading")}</Headline2>
        <Paragraph>{t("DisabilityCostsInfo.Section4.Text")}</Paragraph>
        <List aria-label="second-list">{listDisabilityExpensesMap}</List>

        <Headline2>{t("DisabilityCostsInfo.Section5.Heading")}</Headline2>
        <Paragraph>{t("DisabilityCostsInfo.Section5.Text")}</Paragraph>
        <Paragraph>{t("DisabilityCostsInfo.Section5.Text2")}</Paragraph>

        <Headline2>{t("DisabilityCostsInfo.Section6.Heading")}</Headline2>
        <Paragraph>{t("DisabilityCostsInfo.Section6.Text")}</Paragraph>

        <Headline2>{t("DisabilityCostsInfo.Section7.Heading")}</Headline2>
        <Paragraph>{t("DisabilityCostsInfo.Section7.Text")}</Paragraph>

        <Headline2>{t("DisabilityCostsInfo.Section8.Heading")}</Headline2>
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
