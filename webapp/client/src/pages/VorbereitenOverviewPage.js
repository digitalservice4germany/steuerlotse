import React from "react";
import styled from "styled-components";
import { t } from "i18next";
import { Trans } from "react-i18next";
import PropTypes from "prop-types";
import InfoBox from "../components/InfoBox";
// eslint-disable-next-line import/named
import AnchorButton from "../components/AnchorButton";
import AccordionComponent from "../components/AccordionComponent";
import TileCard from "../components/TileCard";

import VorsorgeaufwendungenIcon from "../assets/icons/vorsorgeaufwendungen.svg";

const ContentWrapper = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 auto;
  max-width: var(--main-max-width);
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
import PropTypes from "prop-types";
padding-top: var(--spacing-06);
  margin: 0;
`;

const TileGrid = styled.div``;

const translationBold = function translationBold(key) {
  return (
    <Trans t={t} i18nKey={key} components={{ bold: <b />, break: <br /> }} />
  );
};

export default function VorbereitenOverviewPage({ downloadPreparationLink }) {
  return (
    <>
      <ContentWrapper>
        <Headline1>{t("vorbereitenOverview.Paragraph1.heading")}</Headline1>
        <Paragraph1>{t("vorbereitenOverview.Paragraph1.text")}</Paragraph1>
        <Headline2>{t("vorbereitenOverview.Paragraph2.heading")}</Headline2>
        <Paragraph2>{t("vorbereitenOverview.Paragraph2.text")}</Paragraph2>
        <AnchorButton
          isDownloadLink
          url={downloadPreparationLink}
          text={t("vorbereitenOverview.Download")}
        />
        <AccordionComponent
          title={t("vorbereitenOverview.Accordion.heading")}
          items={[
            {
              title: t("vorbereitenOverview.Accordion.Item1.heading"),
              detail: translationBold(
                "vorbereitenOverview.Accordion.Item1.detail"
              ),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item2.heading"),
              detail: translationBold(
                "vorbereitenOverview.Accordion.Item2.detail"
              ),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item3.heading"),
              detail: translationBold(
                "vorbereitenOverview.Accordion.Item3.detail"
              ),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item4.heading"),
              detail: translationBold(
                "vorbereitenOverview.Accordion.Item4.detail"
              ),
            },
          ]}
        />
        <Headline2>{t("Krankheitskosten.Paragraph2.heading")}</Headline2>
        <Paragraph2>{t("Krankheitskosten.Paragraph3.text")}</Paragraph2>
        <TileGrid>
          <TileCard title="" icon={VorsorgeaufwendungenIcon} url="" />
        </TileGrid>
      </ContentWrapper>
      <InfoBox />
    </>
  );
}

VorbereitenOverviewPage.propTypes = {
  downloadPreparationLink: PropTypes.string.isRequired,
};
