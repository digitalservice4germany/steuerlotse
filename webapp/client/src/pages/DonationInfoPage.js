import React from "react";
import { t } from "i18next";
import InfoBox from "../components/InfoBox";
// eslint-disable-next-line import/named
import {
  anchorBack,
  anchorList,
  anchorRegister,
} from "../lib/contentPagesAnchors";
import StepHeaderButtons from "../components/StepHeaderButtons";
import {
  AnchorListItem,
  ContentWrapper,
  Headline1,
  Headline2,
  List,
  ListItem,
  Paragraph,
  ParagraphLarge,
} from "../components/ContentPagesGeneralStyling";

export default function DonationInfoPage() {
  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Spenden und Mitgliedsbeiträge")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));
  const list1 = [
    {
      text: t("Spenden.Section2.list.item1"),
    },
    {
      text: t("Spenden.Section2.list.item2"),
    },
    {
      text: t("Spenden.Section2.list.item3"),
    },
    {
      text: t("Spenden.Section2.list.item4"),
    },
    {
      text: t("Spenden.Section2.list.item5"),
    },
  ];
  const listItemsMap = list1.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));
  const list2 = [
    {
      text: t("Spenden.Section2.list2.item1"),
    },
    {
      text: t("Spenden.Section2.list2.item2"),
    },
    {
      text: t("Spenden.Section2.list2.item3"),
    },
    {
      text: t("Spenden.Section2.list2.item4"),
    },
    {
      text: t("Spenden.Section2.list2.item5"),
    },
  ];
  const listItemsSecondMap = list2.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <Headline1>{t("Spenden.Section1.heading")}</Headline1>
        <ParagraphLarge>{t("Spenden.Section1.text")}</ParagraphLarge>
        <Headline2>{t("Spenden.Section2.heading")}</Headline2>
        <Paragraph>{t("Spenden.Section2.text")}</Paragraph>
        <List aria-label="simple-list">{listItemsMap}</List>
        <Paragraph>{t("Spenden.Section2.text2")}</Paragraph>
        <Paragraph spacingVariant>{t("Spenden.Section2.text3")}</Paragraph>
        <List aria-label="simple-list-second">{listItemsSecondMap}</List>
        <Headline2>{t("Spenden.Section3.heading")}</Headline2>
        <Paragraph>{t("Spenden.Section3.text")}</Paragraph>
        <Paragraph>{t("Spenden.Section3.text2")}</Paragraph>
        <Headline2>{t("Spenden.Section4.heading")}</Headline2>
        <Paragraph>{t("Spenden.Section4.text")}</Paragraph>
        <Paragraph>{t("Spenden.Section4.text2")}</Paragraph>
        <Headline2>{t("Handwerkerleistungen.Section5.heading")}</Headline2>
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
