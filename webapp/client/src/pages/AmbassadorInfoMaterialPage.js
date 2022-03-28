import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation, Trans } from "react-i18next";
import { TopSpacing } from "../components/ContentPageStyles";
import DownloadLink from "../components/DownloadLink";
import SecondaryAnchorButton from "../components/SecondaryAnchorButton";

const HeadingText = styled.div`
  font-size: 36px;
  margin: 24px 0;
  line-height: 110%;
`;

const HeroImage = styled.img`
  height: 477px;
`;

const HowItWorksImage = styled.img`
  max-width: 930px;
  width: 930px;
`;

const Intro = styled.div`
  width: 832px;
`;

const Content = styled.div`
  margin-top: 56px;
  display: flex;
  flex-direction: column;
`;

const SubHeadingText = styled.div`
  margin: 24px 0 50px 0;
  font-size: 28px;
`;
const ParagraphHeading = styled.div`
  font-size: 26px;
  margin: 16px 0;
  width: 778px;
  max-width: 778px;
`;
const ContentText = styled.div`
  font-size: 24px;
`;

const VerticallyCentered = styled.div`
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
`;

export default function AmbassadorInfoMaterialPage({ plausibleDomain }) {
  const { t } = useTranslation();
  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          mailToContact: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="mailto:kontakt@steuerlotse-rente.de\" />
          ),
        }}
      />
    );
  }
  return (
    <TopSpacing>
      <Intro>
        <HeadingText className="font-weight-bold">
          {t("AmbassadorMaterial.Heading")}
        </HeadingText>
        <SubHeadingText>{t("AmbassadorMaterial.SubHeading")}</SubHeadingText>
      </Intro>
      <HeroImage
        src="/images/hero-image-botschafter.png"
        alt="Bilder von Rentnerinnen und Rentnern beim Ausfüllen ihrer digitalen Steuererklärung"
      />
      <Content>
        <ParagraphHeading className="font-weight-bold">
          {t("AmbassadorMaterial.Paragraph.DownloadInformationText")}
        </ParagraphHeading>
        <div className="mb-3">
          <DownloadLink
            text={t("AmbassadorMaterial.Paragraph.InfoBroshureDownloadLink")}
            url="/download_pf/print.pdf"
            plausibleDomain={plausibleDomain}
            plausibleName="Download Informationsbroschüre"
          />
        </div>
        <div>
          <DownloadLink
            text={t("AmbassadorMaterial.Paragraph.SteuerlotsenFlyerLink")}
            url="/download_pf/print.pdf"
            plausibleDomain={plausibleDomain}
            plausibleName="Download Steuerlotsen-Flyer"
          />
        </div>
      </Content>
      <Content>
        <ParagraphHeading className="font-weight-bold">
          {t("AmbassadorMaterial.Paragraph.HowItWorks")}
        </ParagraphHeading>
        <div style={{ position: "relative" }}>
          <a
            href="https://www.youtube.com/watch?v=vP--fwSWtLE"
            plausibleDomain={plausibleDomain}
            plausibleName="Youtube-Link clicked"
          >
            <HowItWorksImage
              src="/images/How_It_Works_Video.png"
              alt="Link to How It Works Video"
              href="https://www.youtube.com/watch?v=vP--fwSWtLE"
            />
          </a>
          <VerticallyCentered>
            <SecondaryAnchorButton
              text="Auf Youtube abspielen"
              url="/download_preparation"
              className="outline-0"
              isLinkingOutLink
            />
          </VerticallyCentered>
        </div>
      </Content>
      <Content>
        <ParagraphHeading className="font-weight-bold">
          {t("AmbassadorMaterial.Paragraph.AnyOtherQuestions")}
        </ParagraphHeading>
        <ContentText>
          {trans("AmbassadorMaterial.Paragraph.ContactUs")}
        </ContentText>
      </Content>
    </TopSpacing>
  );
}

AmbassadorInfoMaterialPage.propTypes = {
  plausibleDomain: PropTypes.string,
};

AmbassadorInfoMaterialPage.defaultProps = { plausibleDomain: undefined };
