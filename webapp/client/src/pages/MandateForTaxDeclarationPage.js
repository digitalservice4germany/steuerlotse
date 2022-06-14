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
  HeaderSection,
  TopContent,
  Picture,
  IntroParagraphText,
  ParagraphHeadingH2,
  ParagraphHeadingH3,
  ShareBox,
  ListContent,
} from "../components/ContentPageStyles";
import AccordionComponent from "../components/AccordionComponent";
import ButtonAnchor from "../components/ButtonAnchor";
import { ListItem } from "../components/ContentPagesGeneralStyling";
import InfoBox from "../components/InfoBox";
import { anchorPrufen } from "../lib/contentPagesAnchors";
import SuccessStepsInfoBox from "../components/SuccessStepsInfoBox";
import { ReactComponent as PlayIconInverse } from "../assets/icons/DefaultStatePlayIcon.svg";

const CTAButton = styled(ButtonAnchor)`
  margin-top: var(--spacing-03);
`;

const AnchorList = styled.ul`
  font-size: var(--text-xl);
  margin-top: var(--spacing-06);
  margin-bottom: var(--spacing-06);
`;

export default function MandateForTaxDeclarationPage({ plausibleDomain }) {
  const { t } = useTranslation();

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          bfinm: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/2016-08-01-amtliche-muster-fuer-vollmachten-im-besteuerungsverfahren.html" />
          ),
          vlh: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.vlh.de/krankheit-vorsorge/altersbezuege/wann-muss-ich-als-rentner-steuern-zahlen-und-wie-viel.html" />
          ),
          finanztip: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.finanztip.de/steuererklaerung/rentenbesteuerung/" />
          ),
          mdr: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.mdr.de/nachrichten/deutschland/wirtschaft/rente-rentner-steuer-steuererklaerung-100.html" />
          ),
          steuertipps: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.steuertipps.de/steuern-rente#absatz-7" />
          ),
        }}
      />
    );
  }

  const ListItemsPart2 = [
    {
      text: t("mandateForTaxDeclaration.Body.part2.list.item1"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part2.list.item2"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part2.list.item3"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part2.list.item4"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part2.list.item5"),
    },
    {
      text: trans("mandateForTaxDeclaration.Body.part2.list.item6"),
    },
  ];

  const ListPart2 = ListItemsPart2.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  const ListItemsPart3 = [
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item1"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item2"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item3"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item4"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item5"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item6"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item7"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item8"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item9"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item10"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part3.list.item11"),
    },
  ];

  const ListPart3 = ListItemsPart3.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  const ListItemsPart4 = [
    {
      text: t("mandateForTaxDeclaration.Body.part4.list.item1"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part4.list.item2"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part4.list.item3"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part4.list.item4"),
    },
    {
      text: t("mandateForTaxDeclaration.Body.part4.list.item5"),
    },
  ];

  const ListPart4 = ListItemsPart4.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  const { Text, Icon } = ButtonAnchor;

  return (
    <>
      <Helmet>
        <meta name="title" content={t("mandateForTaxDeclaration.meta.title")} />
        <meta
          name="description"
          content={t("mandateForTaxDeclaration.meta.description")}
        />
        <meta
          name="keywords"
          content={t("mandateForTaxDeclaration.meta.keywords")}
        />
      </Helmet>
      <ContentSpacingWrapper>
        <HeaderSection>
          <TopContent>
            <IntroHeadingText className="h1 mt-5 mb-5">
              {t("mandateForTaxDeclaration.Heading")}
            </IntroHeadingText>
            <IntroParagraphText>
              {t("mandateForTaxDeclaration.Teaser")}
            </IntroParagraphText>
            <Picture>
              <img
                src="../images/mandate-for-tax-declaration.jpg"
                alt="Frau hilft Verwandten am Laptop bei ihrer Steuererklärung"
              />
            </Picture>
          </TopContent>
          <AnchorList>
            <li>
              <a href="#anchor1">
                {t("mandateForTaxDeclaration.AnchorList.anchor1")}
              </a>
            </li>
            <li>
              <a href="#anchor2">
                {t("mandateForTaxDeclaration.AnchorList.anchor2")}
              </a>
            </li>
            <li>
              <a href="#anchor3">
                {t("mandateForTaxDeclaration.AnchorList.anchor3")}
              </a>
            </li>
            <li>
              <a href="#anchor4">
                {t("mandateForTaxDeclaration.AnchorList.anchor4")}
              </a>
            </li>
          </AnchorList>
          <AccordionComponent
            title={t("mandateForTaxDeclaration.Accordion.heading")}
            items={[
              {
                title: t("mandateForTaxDeclaration.Accordion.Item1.heading"),
                detail: t("mandateForTaxDeclaration.Accordion.Item1.detail"),
              },
              {
                title: t("mandateForTaxDeclaration.Accordion.Item2.heading"),
                detail: t("mandateForTaxDeclaration.Accordion.Item2.detail"),
              },
              {
                title: t("mandateForTaxDeclaration.Accordion.Item3.heading"),
                detail: t("mandateForTaxDeclaration.Accordion.Item3.detail"),
              },
              {
                title: t("mandateForTaxDeclaration.Accordion.Item4.heading"),
                detail: trans(
                  "mandateForTaxDeclaration.Accordion.Item4.detail"
                ),
              },
            ]}
          />
        </HeaderSection>

        <ContentText>
          <ParagraphTextLarger className="mt-5">
            {trans("mandateForTaxDeclaration.Body.introText")}
          </ParagraphTextLarger>

          <ParagraphHeadingH2 id="anchor1">
            {t("mandateForTaxDeclaration.Body.part1.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part1.text1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part1.text2")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part1.text3")}
          </ParagraphTextLarger>

          <ShareBox>
            <SuccessStepsInfoBox
              header={t("mandateForTaxDeclaration.Body.ShareBox.header")}
              text={t("mandateForTaxDeclaration.Body.ShareBox.text")}
              promoteUrl={t(
                "mandateForTaxDeclaration.Body.ShareBox.promoteUrl"
              )}
              shareText={t("mandateForTaxDeclaration.Body.ShareBox.shareText")}
              mailSubject={t(
                "mandateForTaxDeclaration.Body.ShareBox.mailSubject"
              )}
              sourcePage={t(
                "mandateForTaxDeclaration.Body.ShareBox.sourcePage"
              )}
              plausibleDomain={plausibleDomain}
              shareBoxSpacingVariant
            />
          </ShareBox>

          <ParagraphHeadingH2>
            {t("mandateForTaxDeclaration.Body.part2.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part2.text1")}
          </ParagraphTextLarger>

          <ListContent aria-label="simple-list">{ListPart2}</ListContent>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part2.text2")}
          </ParagraphTextLarger>

          <ButtonAnchor
            url="https://youtu.be/51VwaRbRxvI"
            plausibleGoal="Youtube-Link MandateForTaxDeclaration clicked"
            plausibleDomain={plausibleDomain}
            variant="outline"
            external
          >
            <Icon>
              <PlayIconInverse />
            </Icon>
            <Text>Erklärvideo auf Youtube abspielen</Text>
          </ButtonAnchor>

          <ParagraphHeadingH2 id="anchor2">
            {t("mandateForTaxDeclaration.Body.part3.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part3.text1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part3.text2")}
          </ParagraphTextLarger>

          <ListContent aria-label="simple-list">{ListPart3}</ListContent>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part3.text3")}
          </ParagraphTextLarger>

          <ParagraphHeadingH3>
            {t("mandateForTaxDeclaration.Body.part3.subHeading1")}
          </ParagraphHeadingH3>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part3.text4")}
          </ParagraphTextLarger>

          <ParagraphHeadingH2 id="anchor3">
            {t("mandateForTaxDeclaration.Body.part4.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part4.text1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part4.text2")}
          </ParagraphTextLarger>

          <ListContent aria-label="simple-list">{ListPart4}</ListContent>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part4.text3")}
          </ParagraphTextLarger>

          <ParagraphHeadingH2 id="anchor4">
            {t("mandateForTaxDeclaration.Body.part5.heading")}
          </ParagraphHeadingH2>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part5.text1")}
          </ParagraphTextLarger>

          <ParagraphTextLarger className="mt-3">
            {trans("mandateForTaxDeclaration.Body.part5.text2")}
          </ParagraphTextLarger>

          <CTAButton
            url={t("mandateForTaxDeclaration.Body.button.url")}
            plausibleGoal={t(
              "mandateForTaxDeclaration.Body.button.plausibleGoal"
            )}
            plausibleDomain={plausibleDomain}
          >
            {t("mandateForTaxDeclaration.Body.button.label")}
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

MandateForTaxDeclarationPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

MandateForTaxDeclarationPage.defaultProps = {
  plausibleDomain: undefined,
};
