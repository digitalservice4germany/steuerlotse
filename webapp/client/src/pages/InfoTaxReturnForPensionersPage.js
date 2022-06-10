import React from "react";
import PropTypes from "prop-types";
import { Trans, useTranslation } from "react-i18next";
import ContentPageBox from "../components/ContentPageBox";
import {
  ContentSpacingWrapper,
  IntroHeadingText,
  IntroParagraphText,
  ContentText,
  ParagraphTextLarger,
  ParagraphHeadingLarger,
  ListBox,
  ListBoxText,
  ShareBox,
  HeaderSection,
  Picture,
  TopContent,
} from "../components/ContentPageStyles";

import SuccessStepsInfoBox from "../components/SuccessStepsInfoBox";

export default function InfoTaxReturnForPensionersPage({ plausibleDomain }) {
  const { t } = useTranslation();
  const buttons = {
    buttonOne: {
      text: t("taxGuideQuestionBox.startQuestionnaire"),
      url: "/eligibility/step/marital_status?link_overview=False",
      plausibleGoal: "contentPage_startQuestionnaire_clicked",
    },
    buttonTwo: {
      text: t("taxGuideQuestionBox.faq"),
      url: "/sofunktionierts",
      plausibleGoal: "contentPage_faq_clicked",
    },
    buttonThree: {
      text: t("taxGuideQuestionBox.contactUs"),
      url: "mailto:kontakt@steuerlotse-rente.de",
      plausibleGoal: "contentPage_contactUs_clicked",
    },
  };

  const boxText = {
    headerOne: t("taxGuideQuestionBox.canIUseTaxGuide"),
    headerTwo: t("taxGuideQuestionBox.moreInformationTaxGuide"),
  };

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          statistaLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://de.statista.com/statistik/daten/studie/4806/umfrage/rentenanpassungen-der-bundesregierung-seit-1999/" />
          ),
          destatisLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.destatis.de/DE/Presse/Pressemitteilungen/2021/08/PD21_380_73111.html" />
          ),
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          downloadPreparationLink: <a href="/download_preparation" />,
          incomeCalculatorLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.finanzamt.bayern.de/Informationen/Steuerinfos/Steuerberechnung/Alterseinkuenfte-Rechner/#button" />
          ),
          pensionersInsuranceLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://www.deutsche-rentenversicherung.de/DRV/DE/Rente/Allgemeine-Informationen/Besteuerung-der-Rente/besteuerung-der-rente_node.html" />
          ),
          eligibilityLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/eligibility/step/tax_year?link_overview=False" />
          ),
          registrationLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_request/step/data_input?link_overview=False" />
          ),
          activationLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_activation/step/data_input?link_overview=False" />
          ),
          shareLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/vereinfachte-steuererklärung-für-rentner" />
          ),
        }}
      />
    );
  }

  return (
    <>
      <ContentSpacingWrapper>
        <HeaderSection>
          <Picture>
            <img
              src="/images/hero_info_tax_return_pensioners.png"
              alt="Bild von Rentnerin und Rentner beim Ausfüllen ihrer digitalen Steuererklärung"
            />
          </Picture>
          <TopContent>
            <IntroHeadingText className="h1 mt-5 mb-4">
              {t("infoTaxReturnPensioners.intro.heading")}
            </IntroHeadingText>
            <IntroParagraphText>
              {trans("infoTaxReturnPensioners.intro.paragraphOne")}
            </IntroParagraphText>
          </TopContent>
        </HeaderSection>
        <ContentText>
          <ParagraphTextLarger className=" mt-5">
            {trans("infoTaxReturnPensioners.intro.paragraphTwo")}
          </ParagraphTextLarger>
          <ParagraphHeadingLarger className="h2 mt-5 mb-3  font-weight-bold">
            {t("infoTaxReturnPensioners.section_two.heading")}
          </ParagraphHeadingLarger>
          <ParagraphTextLarger>
            {trans("infoTaxReturnPensioners.section_two.paragraph")}
          </ParagraphTextLarger>
        </ContentText>
        <ShareBox>
          <SuccessStepsInfoBox
            header={t("infoTaxReturnPensioners.ShareBox.header")}
            text={t("infoTaxReturnPensioners.ShareBox.text")}
            promoteUrl={t("infoTaxReturnPensioners.ShareBox.promoteUrl")}
            shareText={t("infoTaxReturnPensioners.ShareBox.shareText")}
            mailSubject={t("infoTaxReturnPensioners.ShareBox.mailSubject")}
            sourcePage={t("infoTaxReturnPensioners.ShareBox.sourcePage")}
            plausibleDomain={plausibleDomain}
            shareBoxSpacingVariant
          />
        </ShareBox>
        <ContentText>
          <ParagraphHeadingLarger className="h2 mt-5 mb-3  font-weight-bold">
            {t("infoTaxReturnPensioners.section_three.heading")}
          </ParagraphHeadingLarger>
          <ParagraphTextLarger>
            {trans("infoTaxReturnPensioners.section_three.paragraphOne")}
          </ParagraphTextLarger>
          <ParagraphTextLarger>
            {trans("infoTaxReturnPensioners.section_three.paragraphTwo")}
          </ParagraphTextLarger>
          <ParagraphHeadingLarger className="h2 mt-5 mb-3  font-weight-bold">
            {t("infoTaxReturnPensioners.section_four.heading")}
          </ParagraphHeadingLarger>
          <ParagraphTextLarger>
            {trans("infoTaxReturnPensioners.section_four.paragraph")}
          </ParagraphTextLarger>
          <ListBox className="my-5">
            <ListBoxText className="h4 mt-1 mb-3  font-weight-bold">
              {t("infoTaxReturnPensioners.section_five.listItemOneHeading")}
            </ListBoxText>
            <ListBoxText>
              {trans("infoTaxReturnPensioners.section_five.listItemOne")}
            </ListBoxText>
            <ListBoxText className="h4 mt-5 mb-3  font-weight-bold">
              {t("infoTaxReturnPensioners.section_five.listItemTwoHeading")}
            </ListBoxText>
            <ListBoxText>
              {trans("infoTaxReturnPensioners.section_five.listItemTwo")}
            </ListBoxText>
            <ListBoxText className="h4 mt-5 mb-3  font-weight-bold">
              {t("infoTaxReturnPensioners.section_five.listItemThreeHeading")}
            </ListBoxText>
            <ListBoxText>
              {trans("infoTaxReturnPensioners.section_five.listItemThree")}
            </ListBoxText>
            <ListBoxText className="h4 mt-5 mb-3  font-weight-bold">
              {t("infoTaxReturnPensioners.section_five.listItemFourHeading")}
            </ListBoxText>
            <ListBoxText>
              {trans("infoTaxReturnPensioners.section_five.listItemFour")}
            </ListBoxText>
          </ListBox>
          <ParagraphTextLarger className="mb-5 ">
            {trans("infoTaxReturnPensioners.section_six.text")}
          </ParagraphTextLarger>
        </ContentText>
      </ContentSpacingWrapper>
      <ContentPageBox anchor={buttons} boxText={boxText} />
    </>
  );
}

InfoTaxReturnForPensionersPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

InfoTaxReturnForPensionersPage.defaultProps = {
  plausibleDomain: undefined,
};
