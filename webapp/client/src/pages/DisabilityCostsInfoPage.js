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
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function DisabilityCostsInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Kosten aufgrund einer Behinderung")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  const listLumpSumInfo = [
    {
      text: t("DisabilityCostsInfo.Paragraph3.ListItem1"),
    },
    {
      text: t("DisabilityCostsInfo.Paragraph3.ListItem2"),
    },
    {
      text: t("DisabilityCostsInfo.Paragraph3.ListItem3"),
    },
  ];

  const listDisabilityExpenses = [
    {
      text: t("DisabilityCostsInfo.Paragraph4.ListItem1"),
    },
    {
      text: t("DisabilityCostsInfo.Paragraph4.ListItem2"),
    },
    {
      text: t("DisabilityCostsInfo.Paragraph4.ListItem3"),
    },
    {
      text: t("DisabilityCostsInfo.Paragraph4.ListItem4"),
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

        <Headline1>{t("DisabilityCostsInfo.Paragraph1.Heading")}</Headline1>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph1.Text")}
        </Paragraph>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph2.Heading")}
        </Headline2>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph2.Text")}
        </Paragraph>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph3.Heading")}
        </Headline2>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph3.Text")}
        </Paragraph>
        <List aria-label="first-list">{listLumpSumInfoMap}</List>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph4.Heading")}
        </Headline2>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph4.Text")}
        </Paragraph>
        <List aria-label="first-list">{listDisabilityExpensesMap}</List>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph5.Heading")}
        </Headline2>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph5.Text")}
        </Paragraph>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph6.Heading")}
        </Headline2>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph6.Text")}
        </Paragraph>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph7.Heading")}
        </Headline2>
        <Paragraph textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph7.Text")}
        </Paragraph>

        <Headline2 textSizeVariant>
          {t("DisabilityCostsInfo.Paragraph8.Heading")}
        </Headline2>
        <List aria-label="anchor-list">{anchorListItemsMap}</List>
      </ContentWrapper>
      <InfoBox />
    </>
  );
}
