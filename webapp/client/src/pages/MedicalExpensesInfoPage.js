import React from "react";
import { t } from "i18next";
import InfoBox from "../components/InfoBox";
import FormHeader from "../components/FormHeader";

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
  Headline2,
  List,
  ListItem,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function MedicalExpensesInfoPage() {
  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Krankheitskosten")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));
  const list = [
    {
      text: t("Krankheitskosten.List.item1.text"),
    },
    {
      text: t("Krankheitskosten.List.item2.text"),
    },
    {
      text: t("Krankheitskosten.List.item3.text"),
    },
    {
      text: t("Krankheitskosten.List.item4.text"),
    },
    {
      text: t("Krankheitskosten.List.item5.text"),
    },
    {
      text: t("Krankheitskosten.List.item6.text"),
    },
  ];
  const listItemsMap = list.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />

        <FormHeader
          title={t("Krankheitskosten.Paragraph1.heading")}
          intro={t("Krankheitskosten.Paragraph1.text")}
        />

        <Headline2>{t("Krankheitskosten.Paragraph2.heading")}</Headline2>
        <List aria-label="simple-list">{listItemsMap}</List>
        <Headline2>{t("Krankheitskosten.Paragraph3.heading")}</Headline2>
        <Paragraph>{t("Krankheitskosten.Paragraph3.text")}</Paragraph>
        <Headline2>{t("Krankheitskosten.Paragraph4.heading")}</Headline2>
        <Paragraph>{t("Krankheitskosten.Paragraph4.text")}</Paragraph>
        <Headline2>{t("Krankheitskosten.Paragraph5.heading")}</Headline2>
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
