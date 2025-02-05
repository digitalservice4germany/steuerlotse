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
  ListItem,
  Headline2,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function CareCostsInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Pflegekosten")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  const listCareCostExamples = [
    {
      text: t("CareCostsInfo.Paragraph2.ListItem1"),
    },
    {
      text: t("CareCostsInfo.Paragraph2.ListItem2"),
    },
  ];

  const listCareCostItemsMap = listCareCostExamples.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <FormHeader
          title={t("CareCostsInfo.Paragraph1.Heading")}
          intro={t("CareCostsInfo.Paragraph1.Text")}
        />
        <Headline2>{t("CareCostsInfo.Paragraph2.Heading")}</Headline2>
        <List aria-label="simple-list">{listCareCostItemsMap}</List>
        <Headline2>{t("CareCostsInfo.Paragraph3.Heading")}</Headline2>
        <Paragraph>{t("CareCostsInfo.Paragraph3.Text")}</Paragraph>
        <Headline2>{t("CareCostsInfo.Paragraph4.Heading")}</Headline2>
        <Paragraph>{t("CareCostsInfo.Paragraph4.Text")}</Paragraph>
        <Paragraph>{t("CareCostsInfo.Paragraph4.Text2")}</Paragraph>
        <Headline2>{t("CareCostsInfo.Paragraph5.Heading")}</Headline2>
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
