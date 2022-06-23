import React from "react";
import styled from "styled-components";
import { t } from "i18next";
import { Trans } from "react-i18next";
import PropTypes from "prop-types";
import FormHeader from "../components/FormHeader";
import InfoBox from "../components/InfoBox";
import AccordionComponent from "../components/AccordionComponent";
import TileCard from "../components/TileCard";

import VorsorgeaufwendungenIcon from "../assets/icons/vorsorgeaufwendungen.svg";
import KrankheitskostenIcon from "../assets/icons/krankheitskosten.svg";
import PflegekostenIcon from "../assets/icons/pflegekosten.svg";
import AngabenBeiBehinderungIcon from "../assets/icons/angaben_bei_behinderung.svg";
import BestattungskostenIcon from "../assets/icons/bestattungskosten.svg";
import WiederbeschaffungskostenIcon from "../assets/icons/wiederbeschaffungskosten.svg";
import HaushaltsnaheDienstleistungenIcon from "../assets/icons/haushaltsnahe_dienstleistungen.svg";
import HandwerkerleistungenIcon from "../assets/icons/handwerkerleistungen.svg";
import SpendenUndMitgliedsbeitraegeIcon from "../assets/icons/spenden_und_mitgliedsbeitraege.svg";
import KirchensteuerIcon from "../assets/icons/kirchensteuer.svg";
import {
  ContentWrapper,
  Headline2,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";
import ButtonAnchor from "../components/ButtonAnchor";
import { anchorRegister } from "../lib/contentPagesAnchors";

const TileGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  grid-auto-rows: auto;
  grid-gap: 8px;
  padding-top: var(--spacing-06);

  @media screen and (min-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media screen and (min-width: 1136px) {
    grid-template-columns: repeat(3, 1fr);
  }
`;

const ButtonAnchorOverview = styled(ButtonAnchor)`
  margin-top: var(--spacing-04);
`;

export default function VorbereitenOverviewPage({
  downloadPreparationLink,
  vorsorgeaufwendungenUrl,
  krankheitskostenUrl,
  pflegekostenUrl,
  angabenBeiBehinderungUrl,
  bestattungskostenUrl,
  wiederbeschaffungskostenUrl,
  haushaltsnaheDienstleistungenUrl,
  handwerkerleistungenUrl,
  spendenUndMitgliedsbeitraegeUrl,
  kirchensteuerUrl,
}) {
  const { Text } = ButtonAnchor;
  const translateText = function translateText(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          steuerIdLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a
              aria-label="Info zur Steuerliche Identifikationsnummer"
              href="https://www.bzst.de/DE/Privatpersonen/SteuerlicheIdentifikationsnummer/steuerlicheidentifikationsnummer_node.html"
              target="_blank"
              rel="noreferrer"
            />
          ),
        }}
      />
    );
  };

  return (
    <>
      <ContentWrapper>
        <FormHeader
          title={t("vorbereitenOverview.Paragraph1.heading")}
          intro={t("vorbereitenOverview.Paragraph1.text")}
        />
        <Headline2>{t("vorbereitenOverview.Paragraph2.heading")}</Headline2>
        <Paragraph>{t("vorbereitenOverview.Paragraph2.text")}</Paragraph>
        <ButtonAnchorOverview url={downloadPreparationLink} download>
          <Text>{t("vorbereitenOverview.Download")}</Text>
        </ButtonAnchorOverview>
        <AccordionComponent
          title={t("vorbereitenOverview.Accordion.heading")}
          items={[
            {
              title: t("vorbereitenOverview.Accordion.Item1.heading"),
              detail: t("vorbereitenOverview.Accordion.Item1.detail"),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item2.heading"),
              detail: t("vorbereitenOverview.Accordion.Item2.detail"),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item3.heading"),
              detail: translateText(
                "vorbereitenOverview.Accordion.Item3.detail"
              ),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item4.heading"),
              detail: t("vorbereitenOverview.Accordion.Item4.detail"),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item5.heading"),
              detail: t("vorbereitenOverview.Accordion.Item5.detail"),
            },
          ]}
        />
        <Headline2>{t("vorbereitenOverview.Paragraph3.heading")}</Headline2>
        <Paragraph>{t("vorbereitenOverview.Paragraph3.text")}</Paragraph>
        <TileGrid>
          <TileCard
            title="Vorsorgeaufwendungen"
            icon={VorsorgeaufwendungenIcon}
            url={vorsorgeaufwendungenUrl}
          />
          <TileCard
            title="Krankheitskosten"
            icon={KrankheitskostenIcon}
            url={krankheitskostenUrl}
          />
          <TileCard
            title="Pflegekosten"
            icon={PflegekostenIcon}
            url={pflegekostenUrl}
          />
          <TileCard
            title="Angaben bei Behinderung"
            icon={AngabenBeiBehinderungIcon}
            url={angabenBeiBehinderungUrl}
          />
          <TileCard
            title="Bestattungskosten"
            icon={BestattungskostenIcon}
            url={bestattungskostenUrl}
          />
          <TileCard
            title="Wiederbeschaffungskosten"
            icon={WiederbeschaffungskostenIcon}
            url={wiederbeschaffungskostenUrl}
          />
          <TileCard
            title="Haushaltsnahe Dienstleistungen"
            icon={HaushaltsnaheDienstleistungenIcon}
            url={haushaltsnaheDienstleistungenUrl}
          />
          <TileCard
            title="Handwerkerleistungen"
            icon={HandwerkerleistungenIcon}
            url={handwerkerleistungenUrl}
          />
          <TileCard
            title="Spenden und Mitgliedsbeiträge"
            icon={SpendenUndMitgliedsbeitraegeIcon}
            url={spendenUndMitgliedsbeitraegeUrl}
          />
          <TileCard
            title="Kirchensteuer"
            icon={KirchensteuerIcon}
            url={kirchensteuerUrl}
          />
        </TileGrid>
      </ContentWrapper>
      <InfoBox
        boxHeadline={anchorRegister.headline}
        boxText={t("InfoBox.text")}
        anchor={anchorRegister}
      />
    </>
  );
}

VorbereitenOverviewPage.propTypes = {
  downloadPreparationLink: PropTypes.string.isRequired,
  vorsorgeaufwendungenUrl: PropTypes.string.isRequired,
  krankheitskostenUrl: PropTypes.string.isRequired,
  pflegekostenUrl: PropTypes.string.isRequired,
  angabenBeiBehinderungUrl: PropTypes.string.isRequired,
  bestattungskostenUrl: PropTypes.string.isRequired,
  wiederbeschaffungskostenUrl: PropTypes.string.isRequired,
  haushaltsnaheDienstleistungenUrl: PropTypes.string.isRequired,
  handwerkerleistungenUrl: PropTypes.string.isRequired,
  spendenUndMitgliedsbeitraegeUrl: PropTypes.string.isRequired,
  kirchensteuerUrl: PropTypes.string.isRequired,
};
