import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import anchorList from "../lib/contentPagesAnchorList";
// import InfoBox from "../components/InfoBox";
import {
  ContentWrapper,
  List,
  AnchorListItem,
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function VorsorgeaufwendungenPage({ prevUrl }) {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Vorsorgeaufwendungen")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  return (
    <>
      <StepHeaderButtons />
      <ContentWrapper>
        <Headline1>{t("Vorsorgeaufwendungen.Paragraph1.Heading")}</Headline1>
        <Paragraph>{t("Vorsorgeaufwendungen.Paragraph1.Text")}</Paragraph>
        <Headline2>{t("Vorsorgeaufwendungen.Paragraph2.Heading")}</Headline2>
        <List>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph2.ListItem1")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph2.ListItem2")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph2.ListItem3")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph2.ListItem4")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph2.ListItem5")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph2.ListItem6")}</ListItem>
        </List>
        <Headline2>{t("Vorsorgeaufwendungen.Paragraph3.Heading")}</Headline2>
        <Paragraph>{t("Vorsorgeaufwendungen.Paragraph3.Text")}</Paragraph>
        <List>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph3.ListItem1")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph3.ListItem2")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph3.ListItem3")}</ListItem>
          <ListItem>{t("Vorsorgeaufwendungen.Paragraph3.ListItem4")}</ListItem>
        </List>
        <Headline2>{t("Vorsorgeaufwendungen.Paragraph4.Heading")}</Headline2>
        <List>{anchorListItemsMap}</List>
      </ContentWrapper>
      {/* <InfoBox fscRequestUrl={fscRequestUrl} /> */}
    </>
  );
}

VorsorgeaufwendungenPage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
