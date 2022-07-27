import { t } from "i18next";

import styled from "styled-components";
import ButtonAnchor from "./ButtonAnchor";

const Box = styled.div`
  background-color: var(--beige-200);
  padding-top: var(--spacing-09);
`;
const InnerBox = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 auto;
  max-width: var(--pages-max-width);

  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: 1fr 0.5fr 0.5fr 1fr;
    grid-template-rows: 1fr;
  }

  @media (min-width: 769px) {
    margin: 0 auto;
    padding-left: var(--spacing-06);
    padding-right: var(--spacing-06);
  }

  @media (min-width: 1025px) {
    padding-left: var(--spacing-08);
    padding-right: var(--spacing-08);
    grid-gap: 1rem;
  }
`;

const TextBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  grid-column: 1 / 3;

  margin-bottom: var(--spacing-06);

  @media (min-width: 768px) {
    grid-row: 1;
  }
`;
const BoxHeadline = styled.h2`
  padding-bottom: var(--spacing-06);
  margin: 0;
  font-size: var(--text-2xl);

  @media (min-width: 768px) {
    font-size: var(--text-3xl);
  }

  @media (min-width: 1024px) {
    font-size: var(--text-5xl);
  }
`;
const BoxText = styled.span`
  padding-bottom: var(--spacing-06);
`;
const Image = styled.img`
  margin: 0;
  grid-column: 3 / -1;
  grid-row: 1;
  margin-top: var(--spacing-06);
  width: 100%;
`;

export default function InfoBoxGrundsteuer() {
  return (
    <Box>
      <InnerBox>
        <TextBox>
          <BoxHeadline>{t("InfoBoxGrundsteuer.heading")}</BoxHeadline>
          <BoxText>{t("InfoBoxGrundsteuer.text")}</BoxText>
          <ButtonAnchor url="https://www.grundsteuererklaerung-fuer-privateigentum.de/">
            {t("InfoBoxGrundsteuer.button")}
          </ButtonAnchor>
        </TextBox>
        <Image
          src="../images/InfoBox-Image-Grundsteuer.png"
          alt="Tablet mit Webapp der Grundsteuer"
        />
      </InnerBox>
    </Box>
  );
}
