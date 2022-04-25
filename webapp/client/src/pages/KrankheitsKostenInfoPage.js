import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { t } from "i18next";
import InfoBox from "../components/InfoBox";
// eslint-disable-next-line import/named
import { anchorBack, anchorList } from "../lib/contentPagesAnchors";
import StepHeaderButtons from "../components/StepHeaderButtons";

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
const Paragraph = styled.p`
  padding-top: var(--spacing-06);
  margin: 0;
`;

export default function KrankheitsKostenInfoPage({ fscRequestUrl }) {
  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Krankheitskosten")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));
  const list = [
    {
      text: "Selbstgetragene Arztkosten/Behandlungskosten und Zuzahlungen zum Beispiel von Zahnärzt:innen, Logopäd:innen, Physiotherapeut:innen, Heilpraktiker:innen oder Psychotherapeut:innen",
    },
    {
      text: "Rezeptgebühren",
    },
    {
      text: "Notwendige Hilfsmittel wie Brillen, Hörgeräte oder spezielle Schuheinlagen",
    },
    {
      text: "Verschriebene Heilkuren, Massagen, Bäder und Einläufe",
    },
    {
      text: "Eigenanteil bei Zahnersatz",
    },
    {
      text: "Fahrtkosten zum Arzt",
    },
  ];
  const listItemsMap = list.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <Headline1>{t("Krankheitskosten.Paragraph1.heading")}</Headline1>
        <Paragraph>{t("Krankheitskosten.Paragraph1.text")}</Paragraph>
        <Headline2>{t("Krankheitskosten.Paragraph2.heading")}</Headline2>
        <List aria-label="simple-list">{listItemsMap}</List>
        <Headline2>{t("Krankheitskosten.Paragraph3.heading")}</Headline2>
        <Paragraph>{t("Krankheitskosten.Paragraph3.text")}</Paragraph>
        <Headline2>{t("Krankheitskosten.Paragraph4.heading")}</Headline2>
        <Paragraph>{t("Krankheitskosten.Paragraph4.text")}</Paragraph>
        <Headline2>{t("Krankheitskosten.Paragraph5.heading")}</Headline2>
        <List aria-label="anchor-list">{anchorListItemsMap}</List>
      </ContentWrapper>
      <InfoBox fscRequestUrl={fscRequestUrl} />
    </>
  );
}

KrankheitsKostenInfoPage.propTypes = {
  fscRequestUrl: PropTypes.string.isRequired,
};
