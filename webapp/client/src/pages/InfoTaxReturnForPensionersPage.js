import React from "react";
import PropTypes from "prop-types";
import { Trans, useTranslation } from "react-i18next";
import AnchorButton from "../components/AnchorButton";
import SecondaryAnchorButton from "../components/SecondaryAnchorButton";
import {
  ContentTopSpacing,
  HeadingText,
  ParagraphIntroText,
  ContentText,
  ParagraphTextLarger,
  ParagraphHeadingText,
  ListBox,
  ListBoxText,
  QuestionBoxBackground,
  QuestionBoxLayer,
  QuestionBox,
  ParagraphTextMedium,
  QuestionBoxAnchorButtons,
} from "../components/ContentPageStyles";

export default function InfoTaxReturnForPensionersPage({ plausibleDomain }) {
  const { t } = useTranslation();

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
            <a href="/eligibility/step/is_correct_tax_year?link_overview=False" />
          ),
          registrationLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_request/step/data_input?link_overview=False" />
          ),
          activationLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_activation/step/data_input?link_overview=False" />
          ),
        }}
      />
    );
  }

  return (
    <ContentTopSpacing>
      <img
        src="/images/hero_info_tax_return_pensioners.png"
        alt="Bild von Rentnerin und Rentner beim Ausfüllen ihrer digitalen Steuererklärung"
      />
      <HeadingText className="h1 mt-5 mb-4">
        {t("infoTaxReturnPensioners.intro.heading")}
      </HeadingText>
      <ParagraphIntroText>
        {trans("infoTaxReturnPensioners.intro.paragraphOne")}
      </ParagraphIntroText>
      <ContentText>
        <ParagraphTextLarger className=" mt-5">
          {trans("infoTaxReturnPensioners.intro.paragraphTwo")}
        </ParagraphTextLarger>
        <ParagraphHeadingText className="h2 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_two.heading")}
        </ParagraphHeadingText>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_two.paragraph")}
        </ParagraphTextLarger>
        <ParagraphHeadingText className="h2 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_three.heading")}
        </ParagraphHeadingText>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_three.paragraphOne")}
        </ParagraphTextLarger>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_three.paragraphTwo")}
        </ParagraphTextLarger>
        <ParagraphHeadingText className="h2 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_four.heading")}
        </ParagraphHeadingText>
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
      <QuestionBoxBackground>
        <QuestionBoxLayer>
          <QuestionBox>
            <div className="mb-5">
              <ParagraphTextMedium className="h4 mb-4 font-weight-bold">
                {t("taxGuideQuestionBox.canIUseTaxGuide")}
              </ParagraphTextMedium>
              <AnchorButton
                url="/eligibility/step/marital_status?link_overview=False"
                text={t("taxGuideQuestionBox.startQuestionnaire")}
                plausibleGoal="contentPage_startQuestionnaire_clicked"
                plausibleDomain={plausibleDomain}
              />
            </div>
            <div className="mt-5">
              <ParagraphTextMedium className="mb-4">
                {trans("taxGuideQuestionBox.moreInformationTaxGuide")}
              </ParagraphTextMedium>
              <QuestionBoxAnchorButtons>
                <SecondaryAnchorButton
                  url="/sofunktionierts"
                  text={t("taxGuideQuestionBox.faq")}
                  plausibleName="contentPage_faq_clicked"
                  plausibleDomain={plausibleDomain}
                />
                <SecondaryAnchorButton
                  url="mailto:kontakt@steuerlotse-rente.de"
                  text={t("taxGuideQuestionBox.contactUs")}
                  plausibleName="contentPage_contactUs_clicked"
                  plausibleDomain={plausibleDomain}
                  className="mt-4 mt-md-0"
                />
              </QuestionBoxAnchorButtons>
            </div>
          </QuestionBox>
        </QuestionBoxLayer>
      </QuestionBoxBackground>
    </ContentTopSpacing>
  );
}

InfoTaxReturnForPensionersPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

InfoTaxReturnForPensionersPage.defaultProps = {
  plausibleDomain: undefined,
};
