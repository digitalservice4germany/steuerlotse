import React from "react";
import styled from "styled-components";
import { t } from "i18next";
import PropTypes from "prop-types";
import InfoBox from "../components/InfoBox";
// eslint-disable-next-line import/named
import AnchorButton from "../components/AnchorButton";
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
  padding-top: 4rem;
  margin: 0;
`;

const Paragraph1 = styled.p`
  font-size: 1.75rem;
  padding-top: 2rem;
  margin: 0;
`;

const Paragraph2 = styled.p`
  padding-top: var(--spacing-03);
  margin-bottom: var(--spacing-03);
`;

const TileGrid = styled.div`
  display: flex;
  flex-wrap: wrap;
  margin-top: 2rem;
  gap: 8px;
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
              detail: t("vorbereitenOverview.Accordion.Item1.detail"),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item2.heading"),
              detail: t("vorbereitenOverview.Accordion.Item2.detail"),
            },
            {
              title: t("vorbereitenOverview.Accordion.Item3.heading"),
              detail: t("vorbereitenOverview.Accordion.Item3.detail"),
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
        <Paragraph2>{t("vorbereitenOverview.Paragraph3.text")}</Paragraph2>
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
      <InfoBox />
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
