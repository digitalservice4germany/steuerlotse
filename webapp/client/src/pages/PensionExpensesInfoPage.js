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

export default function PensionExpensesInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Vorsorgeaufwendungen")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  const listDeductables = [
    {
      text: t("Vorsorgeaufwendungen.Paragraph2.ListItem1"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph2.ListItem2"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph2.ListItem3"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph2.ListItem4"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph2.ListItem5"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph2.ListItem6"),
    },
  ];

  const listNonDeductables = [
    {
      text: t("Vorsorgeaufwendungen.Paragraph3.ListItem1"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph3.ListItem2"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph3.ListItem3"),
    },
    {
      text: t("Vorsorgeaufwendungen.Paragraph3.ListItem4"),
    },
  ];

  const listDeductablesItemsMap = listDeductables.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  const listNonDeductablesItemsMap = listNonDeductables.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <Headline1>{t("Vorsorgeaufwendungen.Paragraph1.Heading")}</Headline1>
        <ParagraphLarge>
          {t("Vorsorgeaufwendungen.Paragraph1.Text")}
        </ParagraphLarge>
        <Headline2>{t("Vorsorgeaufwendungen.Paragraph2.Heading")}</Headline2>
        <List aria-label="first-list">{listDeductablesItemsMap}</List>
        <Headline2>{t("Vorsorgeaufwendungen.Paragraph3.Heading")}</Headline2>
        <Paragraph>{t("Vorsorgeaufwendungen.Paragraph3.Text")}</Paragraph>
        <List aria-label="second-list">{listNonDeductablesItemsMap}</List>
        <Headline2>{t("Vorsorgeaufwendungen.Paragraph4.Heading")}</Headline2>
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
