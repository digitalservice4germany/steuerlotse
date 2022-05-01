import React from "react";
import { t } from "i18next";
import { Trans } from "react-i18next";
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

export default function CraftsmanServicesInfoPage() {
  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Handwerkerleistungen")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));
  const list = [
    {
      text: t("Handwerkerleistungen.Section2.list.item1"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item2"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item3"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item4"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item5"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item6"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item7"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item8"),
    },
    {
      text: t("Handwerkerleistungen.Section2.list.item9"),
    },
  ];
  const listItemsMap = list.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <Headline1>{t("Handwerkerleistungen.Section1.heading")}</Headline1>
        <ParagraphLarge>
          {t("Handwerkerleistungen.Section1.text")}
        </ParagraphLarge>
        <Headline2>{t("Handwerkerleistungen.Section2.heading")}</Headline2>
        <Paragraph>{t("Handwerkerleistungen.Section2.text")}</Paragraph>
        <List aria-label="simple-list">{listItemsMap}</List>
        <Paragraph>
          {" "}
          <Trans
            t={t}
            i18nKey="Handwerkerleistungen.Section2.text2"
            components={{
              bold: <b />,
            }}
          />
        </Paragraph>
        <Paragraph>{t("Handwerkerleistungen.Section2.text3")}</Paragraph>
        <Headline2>{t("Handwerkerleistungen.Section3.heading")}</Headline2>
        <Paragraph>{t("Handwerkerleistungen.Section3.text")}</Paragraph>
        <Paragraph>{t("Handwerkerleistungen.Section3.text2")}</Paragraph>
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
