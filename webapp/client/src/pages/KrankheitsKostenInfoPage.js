import React from "react";
import styled from "styled-components";
import PropTypes, { object } from "prop-types";
import { t } from "i18next";
import InfoBox from "../components/InfoBox";

const ContentWrapper = styled.div`
  padding: var(--spacing-06) var(--spacing-12) 0 var(--spacing-09);
`;
const LinkList = styled.ul`
  margin: 0;
  padding: 0;
`;
const ListItem = styled.li`
  list-style: none;
  padding-bottom: var(--spacing-01);
`;

export default function KrankheitsKostenInfoPage({ fscRequestUrl, linkList }) {
  const listItems = linkList.map((link) => (
    <ListItem>
      <a href={link.url}>{link.text}</a>
    </ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <h1>{t("Krankheitskosten.Paragraph1.heading")}</h1>
        <p>{t("Krankheitskosten.Paragraph1.text")}</p>
        <h2>{t("Krankheitskosten.Paragraph2.heading")}</h2>
        <h2>{t("Krankheitskosten.Paragraph3.heading")}</h2>
        <p>{t("Krankheitskosten.Paragraph3.text")}</p>
        <h2>{t("Krankheitskosten.Paragraph4.heading")}</h2>
        <p>{t("Krankheitskosten.Paragraph4.text")}</p>
        <h2>{t("Krankheitskosten.Paragraph5.heading")}</h2>
        <LinkList>{listItems}</LinkList>
      </ContentWrapper>
      <InfoBox fscRequestUrl={fscRequestUrl} />
    </>
  );
}

KrankheitsKostenInfoPage.propTypes = {
  fscRequestUrl: PropTypes.string.isRequired,
  linkList: PropTypes.arrayOf(object).isRequired,
};
