import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import PropTypes from "prop-types";
import { Helmet } from "react-helmet";
import {
  ContentSpacingWrapper,
  IntroHeadingText,
  ContentText,
  ParagraphTextLarger,
  ListBox,
  ShareBox,
  IntroParagraphText,
  HeaderSection,
  TopContent,
  Picture,
  ParagraphHeadingH2,
  ParagraphHeadingH3,
} from "../components/ContentPageStyles";
import AccordionComponent from "../components/AccordionComponent";
import ButtonAnchor from "../components/ButtonAnchor";
import SuccessStepsInfoBox from "../components/SuccessStepsInfoBox";
import InfoBox from "../components/InfoBox";
import { anchorPrufen } from "../lib/contentPagesAnchors";

const IntroParagraphTextWithMarginTop = styled(IntroParagraphText)`
  padding-top: var(--spacing-07);
`;

const CTAButton = styled(ButtonAnchor)`
  margin-top: var(--spacing-03);
`;

const AnchorList = styled.ul`
  font-size: var(--text-xl);
  margin-top: var(--spacing-06);
  margin-bottom: var(--spacing-06);
`;

export default function FreeTaxDeclarationForPensionersPage({
  plausibleDomain,
}) {
  const { t } = useTranslation();

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          destatisLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.destatis.de/DE/Presse/Pressemitteilungen/2021/08/PD21_380_73111.html" />
          ),
          deutscheRente: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.deutsche-rentenversicherung.de/DRV/DE/Rente/Allgemeine-Informationen/Besteuerung-der-Rente/besteuerung-der-rente_node.html" />
          ),
          bold: <b />,
          elster: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.elster.de/eportal/start" />
          ),
          bfinv: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.formulare-bfinv.de/ffw/content.do" />
          ),
          steuerlotse: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.steuerlotse-rente.de/" />
          ),
          steuerlotseRegister: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.steuerlotse-rente.de/unlock_code_request/step/data_input?link_overview=False" />
          ),
          bfinm: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.bundesfinanzministerium.de/Content/DE/Standardartikel/Themen/Steuern/was-aendert-sich-2022.html" />
          ),
        }}
      />
    );
  }

  return (
    <>
      <Helmet>
        <meta
          name="title"
          content={t("freeTaxDeclarationForPensioners.meta.title")}
        />
        <meta
          name="description"
          content={t("freeTaxDeclarationForPensioners.meta.description")}
        />
        <meta
          name="keywords"
          content={t("freeTaxDeclarationForPensioners.meta.keywords")}
        />
      </Helmet>
      <ContentSpacingWrapper>
        <HeaderSection>
          <TopContent>
            <IntroHeadingText className="h1 mt-5 mb-5">
              {t("freeTaxDeclarationForPensioners.Heading")}
            </IntroHeadingText>
            <Picture>
              <img
                src="/images/free-tax-declaration-for-pensioners.jpeg"
                alt="Bild von Rentnerin und Rentner beim Ausfüllen ihrer digitalen Steuererklärung"
              />
            </Picture>
            <IntroParagraphTextWithMarginTop>
              {t("freeTaxDeclarationForPensioners.Teaser")}
            </IntroParagraphTextWithMarginTop>
          </TopContent>
          <AnchorList>
            <li>
              <a href="#anchor1">
                {t("freeTaxDeclarationForPensioners.AnchorList.anchor1")}
              </a>
            </li>
            <li>
              <a href="#anchor2">
                {t("freeTaxDeclarationForPensioners.AnchorList.anchor2")}
              </a>
            </li>
            <li>
              <a href="#anchor3">
                {t("freeTaxDeclarationForPensioners.AnchorList.anchor3")}
              </a>
            </li>
          </AnchorList>
          <AccordionComponent
            title={t("freeTaxDeclarationForPensioners.Accordion.heading")}
            items={[
              {
                title: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item1.heading"
                ),
                detail: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item1.detail"
                ),
              },
              {
                title: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item2.heading"
                ),
                detail: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item2.detail"
                ),
              },
              {
                title: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item3.heading"
                ),
                detail: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item3.detail"
                ),
              },
              {
                title: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item4.heading"
                ),
                detail: t(
                  "freeTaxDeclarationForPensioners.Accordion.Item4.detail"
                ),
              },
            ]}
          />
        </HeaderSection>

        <ContentText>
          <ParagraphTextLarger className="mt-5">
            {trans("freeTaxDeclarationForPensioners.Body.introText")}
          </ParagraphTextLarger>

          <ParagraphHeadingH2 id="anchor1">
            {t("freeTaxDeclarationForPensioners.Body.part1.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.introText")}
          </ParagraphTextLarger>

          <ParagraphHeadingH3>
            {t("freeTaxDeclarationForPensioners.Body.part1.subHeading1")}
          </ParagraphHeadingH3>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.text1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.example1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.text2")}
          </ParagraphTextLarger>

          <ShareBox>
            <SuccessStepsInfoBox
              header={t("freeTaxDeclarationForPensioners.Body.ShareBox.header")}
              text={t("freeTaxDeclarationForPensioners.Body.ShareBox.text")}
              promoteUrl={t(
                "freeTaxDeclarationForPensioners.Body.ShareBox.promoteUrl"
              )}
              shareText={t(
                "freeTaxDeclarationForPensioners.Body.ShareBox.shareText"
              )}
              mailSubject={t(
                "freeTaxDeclarationForPensioners.Body.ShareBox.mailSubject"
              )}
              sourcePage={t(
                "freeTaxDeclarationForPensioners.Body.ShareBox.sourcePage"
              )}
              plausibleDomain={plausibleDomain}
              shareBoxSpacingVariant
            />
          </ShareBox>

          <ParagraphHeadingH3>
            {t("freeTaxDeclarationForPensioners.Body.part1.subHeading2")}
          </ParagraphHeadingH3>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.text3")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.example2")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part1.text4")}
          </ParagraphTextLarger>

          <ParagraphHeadingH2 id="anchor2">
            {t("freeTaxDeclarationForPensioners.Body.part2.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part2.introText")}
          </ParagraphTextLarger>

          <ParagraphHeadingH3>
            {t("freeTaxDeclarationForPensioners.Body.part2.subHeading1")}
          </ParagraphHeadingH3>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part2.text1")}
          </ParagraphTextLarger>

          <ListBox className="my-5">
            <ParagraphTextLarger className="mt-3">
              {trans("freeTaxDeclarationForPensioners.Body.part2.tipp")}
            </ParagraphTextLarger>
          </ListBox>

          <ParagraphHeadingH3>
            {t("freeTaxDeclarationForPensioners.Body.part2.subHeading2")}
          </ParagraphHeadingH3>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part2.text2")}
          </ParagraphTextLarger>

          <ParagraphHeadingH2 id="anchor3">
            {t("freeTaxDeclarationForPensioners.Body.part3.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part3.introText")}
          </ParagraphTextLarger>

          <ParagraphHeadingH3>
            {t("freeTaxDeclarationForPensioners.Body.part3.subHeading1")}
          </ParagraphHeadingH3>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part3.text1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("freeTaxDeclarationForPensioners.Body.part3.text2")}
          </ParagraphTextLarger>

          <CTAButton
            url={t("freeTaxDeclarationForPensioners.Body.button.url")}
            plausibleGoal={t(
              "freeTaxDeclarationForPensioners.Body.button.plausibleGoal"
            )}
            plausibleDomain={plausibleDomain}
          >
            {t("freeTaxDeclarationForPensioners.Body.button.label")}
          </CTAButton>
        </ContentText>
      </ContentSpacingWrapper>
      <InfoBox
        boxHeadline={anchorPrufen.headline}
        boxText={t("CheckNowInfoBox.text")}
        anchor={anchorPrufen}
      />
    </>
  );
}

FreeTaxDeclarationForPensionersPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

FreeTaxDeclarationForPensionersPage.defaultProps = {
  plausibleDomain: undefined,
};
