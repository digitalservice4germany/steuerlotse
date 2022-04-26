/* import React from "react";
import styled from "styled-components";
import { t } from "i18next";
import InfoBox from "../components/InfoBox";
// eslint-disable-next-line import/named
import { anchorBack, anchorList } from "../lib/contentPagesAnchors";
import StepHeaderButtons from "../components/StepHeaderButtons";
import AnchorButton from "../components/AnchorButton";

const ContentWrapper = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 auto;
  max-width: var(--main-max-width);
`;
const List = styled.ul`
  margin: 0;
  padding: var(--spacing-06) 0 0;
`;
const AnchorListItem = styled.li`
  padding-top: var(--spacing-01);
  list-style: none;
`;
const ListItem = styled.li`
  padding-top: var(--spacing-01);
  list-style-position: inside;
  padding-left: 1.28571429em;
  text-indent: -1.28571429em;
`;
const Headline1 = styled.h1`
  margin: 0;
`;
const Headline2 = styled.h2`
  padding-top: var(--spacing-09);
  margin: 0;
`;
const Paragraph1 = styled.p`
  font-size: 28px;
  padding-top: var(--spacing-06);
  margin: 0;
`;
const Paragraph2 = styled.p`
  padding-top: var(--spacing-06);
  margin: 0;
`;


export default function VorbereitenOverviewPage() {
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
        <Headline1>{t("Krankheitskosten.Paragraph1.heading")}</Headline1>
        <Paragraph1>{t("Krankheitskosten.Paragraph1.text")}</Paragraph1>
        <Headline2>{t("Krankheitskosten.Paragraph2.heading")}</Headline2>
        <Paragraph2>{t("Krankheitskosten.Paragraph3.text")}</Paragraph2>

        <AnchorButton 
          isDownloadLink={true}
          url={"downloadLink"}
          text={t("Krankheitskosten.Paragraph3.text")}
          plausibleGoal={"plausibleGoal"}
          plausibleProps={"plausibleProps"}
          plausibleDomain={"plausibleDomain"}
        ></AnchorButton>

        <Headline1>{t("Krankheitskosten.Paragraph1.heading")}</Headline1>

        <Headline2>{t("Krankheitskosten.Paragraph4.heading")}</Headline2>
        <Paragraph>{t("Krankheitskosten.Paragraph4.text")}</Paragraph>
        <Headline2>{t("Krankheitskosten.Paragraph5.heading")}</Headline2>
        <List aria-label="anchor-list">{anchorListItemsMap}</List>
      </ContentWrapper>
      <InfoBox />
    </>
  );
} */
