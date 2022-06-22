import React from "react";
import { useTranslation } from "react-i18next";
import InfoBox from "../components/InfoBox";
import FormHeader from "../components/FormHeader";
import { anchorPrufen } from "../lib/contentPagesAnchors";
import {
  ContentWrapper,
  List,
  ListItem,
  Headline2,
} from "../components/ContentPagesGeneralStyling";

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
        <FormHeader
          title={t("InfoForRelatives.Section1.Heading")}
          intro={t("InfoForRelatives.Section1.Text")}
        />
        <Headline2 noMargin>{t("InfoForRelatives.Section2.Heading")}</Headline2>
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
