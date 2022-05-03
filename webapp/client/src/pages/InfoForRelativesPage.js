import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import InfoBox from "../components/InfoBox";
import {
  ContentWrapper,
  List,
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
  ParagraphLarge,
} from "../components/ContentPagesGeneralStyling";
import { anchorPrufen } from "../lib/contentPagesAnchors";

const Picture = styled.picture`
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
`;

const InnerHeader = styled.div`
  margin-top: var(--spacing-09);
  margin-bottom: var(--spacing-08);

  @media screen and (min-width: 1024px) {
    margin-top: var(--spacing-11);
  }
`;

export default function InfoForRelativesPage() {
  const { t } = useTranslation();

  const ListDependents = [
    {
      text: t("InfoForRelatives.Section2.ListItem1"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem2"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem3"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem4"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem5"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem6"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem7"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem8"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem9"),
    },
  ];

  const ListDependentsMap = ListDependents.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <div>
      <ContentWrapper>
        <InnerHeader>
          <Headline1>{t("InfoForRelatives.Section1.Heading")}</Headline1>
          <ParagraphLarge>{t("InfoForRelatives.Section1.Text")}</ParagraphLarge>
        </InnerHeader>
        <Picture>
          <img
            src="../images/info-angehoerige.jpg"
            alt="Frau hilft Verwandten am Laptop bei ihrer Steuererklärung"
          />
        </Picture>
      </ContentWrapper>
      <ContentWrapper>
        <Headline2>{t("InfoForRelatives.Section2.Heading")}</Headline2>
        <Paragraph>{t("InfoForRelatives.Section2.Text")}</Paragraph>
        <List aria-label="simple-list">{ListDependentsMap}</List>
      </ContentWrapper>
      <InfoBox
        boxHeadline={anchorPrufen.headline}
        boxText={t("CheckNowInfoBox.text")}
        anchor={anchorPrufen}
      />
    </div>
  );
}
