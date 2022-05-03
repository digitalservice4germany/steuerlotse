import React from "react";
import styled from "styled-components";
import { t } from "i18next";
import PropTypes from "prop-types";
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
  Headline1,
  Headline2,
  Paragraph,
  ParagraphLarge,
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
  margin-top: var(--spacing-03);
`;

const Headline1Overview = styled(Headline1)`
  margin-top: var(--spacing-09);

  @media screen and (min-width: 1024px) {
    margin-top: calc(var(--spacing-09) + 5rem);
  }
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

  return (
    <>
      <ContentWrapper>
        <Headline1Overview>
          {t("vorbereitenOverview.Paragraph1.heading")}
        </Headline1Overview>
        <ParagraphLarge>
          {t("vorbereitenOverview.Paragraph1.text")}
        </ParagraphLarge>
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
