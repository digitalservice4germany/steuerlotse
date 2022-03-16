import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import { Trans, useTranslation } from "react-i18next";
import AnchorButton from "../components/AnchorButton";

const QuestionBox = styled.div`
  padding: 50px 0;
`;

const QuestionBoxBackground = styled.div`
  background: var(--bg-highlight-color);
  height: 459px;
  width: calc(100vw - 220px);
  position: relative;
  left: calc(-50vw + 82%);

  display: flex;
  justify-content: center;

  @media (max-width: 1042px) {
    left: calc(-50vw + 85.2%);
  }

  @media (max-width: 1024px) {
    // left: calc(-50vw + 85%);
    left: -1.75rem;
    width: 100vw;
  }

  @media (max-width: 900px) {
    left: -1rem;
    width: 100vw;
  }

  @media (max-width: 360px) {
    height: 615px;
  }
`;

const HeadingText = styled.h1`
  font-size: 2.25rem;
  @media (max-width: 320px) {
    font-size: 2.25rem;
  }
`;
const ParagraphHeadingText = styled.p`
  font-size: 1.75rem;
  @media (max-width: 320px) {
    font-size: 1.5rem;
  }
`;
const ParagraphTextLarger = styled.p`
  font-size: 1.5rem;

  @media (max-width: 320px) {
    font-size: 1.25rem;
  }
`;

const ParagraphTextMedium = styled.p`
  font-size: 1.25rem;
`;

const TestBack = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: auto;
  flex: 1;
  width: 100%;
  max-width: var(--main-max-width);
`;

const ContentTopSpacing = styled.div`
  margin-top: 9.375rem;
  position: relative;

  & img {
    width: 100%;
  }
`;

const QuestionBoxAnchorButtons = styled.div`
  @media (max-width: 605px) {
    display: flex;
    flex-direction: column;
  }
`;

const ListBox = styled.div`
  background: var(--bg-highlight-color);
  padding: 32px;
  list-style-type: none;

  @media (max-width: 320px) {
    padding: 16px;
  }
`;

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
            <a href="/eligibility/step/welcome?link_overview=False" />
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
      <img src="/images/hero_info_tax_return_pensioners.png" alt="hero_image" />
      <HeadingText className="h1 mt-5 mb-4">
        {t("infoTaxReturnPensioners.intro.heading")}
      </HeadingText>
      <ParagraphHeadingText>
        {trans("infoTaxReturnPensioners.intro.paragraphOne")}
      </ParagraphHeadingText>
      <ParagraphTextLarger className=" mt-5">
        {trans("infoTaxReturnPensioners.intro.paragraphTwo")}
      </ParagraphTextLarger>
      <ParagraphTextLarger className="mt-5 mb-3  font-weight-bold">
        {t("infoTaxReturnPensioners.section_two.heading")}
      </ParagraphTextLarger>
      <ParagraphTextLarger>
        {trans("infoTaxReturnPensioners.section_two.paragraph")}
      </ParagraphTextLarger>
      <ParagraphTextLarger className="h4 mt-5 mb-3  font-weight-bold">
        {t("infoTaxReturnPensioners.section_three.heading")}
      </ParagraphTextLarger>
      <ParagraphTextLarger>
        {trans("infoTaxReturnPensioners.section_three.paragraphOne")}
      </ParagraphTextLarger>
      <ParagraphTextLarger>
        {trans("infoTaxReturnPensioners.section_three.paragraphTwo")}
      </ParagraphTextLarger>
      <ParagraphTextLarger className="h4 mt-5 mb-3  font-weight-bold">
        {t("infoTaxReturnPensioners.section_four.heading")}
      </ParagraphTextLarger>
      <ParagraphTextLarger>
        {trans("infoTaxReturnPensioners.section_four.paragraph")}
      </ParagraphTextLarger>
      <ListBox className="my-5">
        <ParagraphTextLarger className="h4 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_five.listItemOneHeading")}
        </ParagraphTextLarger>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_five.listItemOne")}
        </ParagraphTextLarger>
        <ParagraphTextLarger className="h4 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_five.listItemTwoHeading")}
        </ParagraphTextLarger>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_five.listItemTwo")}
        </ParagraphTextLarger>
        <ParagraphTextLarger className="h4 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_five.listItemThreeHeading")}
        </ParagraphTextLarger>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_five.listItemThree")}
        </ParagraphTextLarger>
        <ParagraphTextLarger className="h4 mt-5 mb-3  font-weight-bold">
          {t("infoTaxReturnPensioners.section_five.listItemFourHeading")}
        </ParagraphTextLarger>
        <ParagraphTextLarger>
          {trans("infoTaxReturnPensioners.section_five.listItemFour")}
        </ParagraphTextLarger>
      </ListBox>
      <ParagraphTextLarger className="mb-5 ">
        {trans("infoTaxReturnPensioners.section_six.text")}
      </ParagraphTextLarger>
      <QuestionBoxBackground>
        <TestBack>
          <QuestionBox>
            <div className="mb-5">
              <ParagraphTextMedium className="h4 mb-4 font-weight-bold">
                {t("taxGuideQuestionBox.canIUseTaxGuide")}
              </ParagraphTextMedium>
              <AnchorButton
                url="/eligibility/step/marital_status?link_overview=False"
                text={t("taxGuideQuestionBox.startQuestionnaire")}
                plausibleName="contentPage_startQuestionnaire_clicked"
                plausibleDomain={plausibleDomain}
              />
            </div>
            <div className="mt-5">
              <ParagraphTextMedium className="mb-4">
                {trans("taxGuideQuestionBox.moreInformationTaxGuide")}
              </ParagraphTextMedium>
              <QuestionBoxAnchorButtons>
                <AnchorButton
                  url="/sofunktionierts"
                  text={t("taxGuideQuestionBox.faq")}
                  isSecondaryButton
                  plausibleName="contentPage_faq_clicked"
                  plausibleDomain={plausibleDomain}
                />
                <AnchorButton
                  url="mailto:kontakt@steuerlotse-rente.de"
                  text={t("taxGuideQuestionBox.contactUs")}
                  isSecondaryButton
                  plausibleName="contentPage_contactUs_clicked"
                  plausibleDomain={plausibleDomain}
                  className="mt-4 mt-md-0"
                />
              </QuestionBoxAnchorButtons>
            </div>
          </QuestionBox>
        </TestBack>
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
