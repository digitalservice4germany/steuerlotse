import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import {
  ContentWrapper,
  List,
  ListItem,
  Headline1,
  Headline2,
  ParagraphLarge,
} from "../components/ContentPagesGeneralStyling";

const InnerHeader = styled.div`
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
      <ContentWrapper bottomMargin>
        <InnerHeader>
          <Headline1>{t("InfoForRelatives.Section1.Heading")}</Headline1>
          <ParagraphLarge>{t("InfoForRelatives.Section1.Text")}</ParagraphLarge>
        </InnerHeader>

        <Headline2 noMargin>{t("InfoForRelatives.Section2.Heading")}</Headline2>
        <List aria-label="simple-list">{ListDependentsMap}</List>
      </ContentWrapper>
    </div>
  );
}
