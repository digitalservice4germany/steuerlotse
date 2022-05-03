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

export default function FuneralExpensesInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Bestattungskosten")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  const listDeductables = [
    {
      text: t("Bestattungskosten.Section2.list.item1"),
    },
    {
      text: t("Bestattungskosten.Section2.list.item2"),
    },
    {
      text: t("Bestattungskosten.Section2.list.item3"),
    },
  ];

  const listNonDeductables = [
    {
      text: t("Bestattungskosten.Section3.list.item1"),
    },
    {
      text: t("Bestattungskosten.Section3.list.item2"),
    },
    {
      text: t("Bestattungskosten.Section3.list.item3"),
    },
    {
      text: t("Bestattungskosten.Section3.list.item4"),
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
        <Headline1>{t("Bestattungskosten.Section1.heading")}</Headline1>
        <ParagraphLarge>{t("Bestattungskosten.Section1.text")}</ParagraphLarge>
        <Headline2>{t("Bestattungskosten.Section2.heading")}</Headline2>
        <Paragraph>{t("Bestattungskosten.Section2.text")}</Paragraph>
        <List aria-label="simple-list">{listDeductablesItemsMap}</List>
        <Headline2>{t("Bestattungskosten.Section3.heading")}</Headline2>
        <Paragraph>{t("Bestattungskosten.Section3.text")}</Paragraph>
        <List aria-label="simple-list-second">
          {listNonDeductablesItemsMap}
        </List>
        <Headline2>{t("Bestattungskosten.Section4.heading")}</Headline2>
        <Paragraph>{t("Bestattungskosten.Section4.text")}</Paragraph>
        <Paragraph>{t("Bestattungskosten.Section4.text2")}</Paragraph>
        <Headline2>{t("Bestattungskosten.Section5.heading")}</Headline2>
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
