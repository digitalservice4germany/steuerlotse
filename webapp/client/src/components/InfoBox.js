import styled from "styled-components";
import { t } from "i18next";
import ButtonAnchor from "./ButtonAnchor";
import { anchorRegister } from "../lib/contentPagesAnchors";

const Box = styled.div`
  background-color: var(--beige-200);
  margin-top: var(--spacing-11);
`;
const InnerBox = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 var(--spacing-03);

  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: [first-column] 1.5fr [second-column] 1fr [between-column] 50px [third-column] 70px [fourth-column] 1fr [last-column] 170px [column-end];
    grid-template-rows: [row0] 60px [row1-start] 110px [row1-end] 60px [second-line] 80px [third-line] 125px [fourth-line] 100px [row-end];
  }

  @media (min-width: 1224px) {
    margin: 0 var(--spacing-03) 0 var(--spacing-11);
  }
`;

const Picture = styled.picture`
  margin: var(--spacing-09) 0 0;
  display: block;

  @media (min-width: 768px) {
    grid-column-start: between-column;
    grid-column-end: column-end;
    grid-row-start: row1-end;
    grid-row-end: row-end;
    align-self: end;
    margin: 0;
  }

  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
`;
const BoxHeadline = styled.h2`
  padding-bottom: var(--spacing-06);
  padding-top: var(--spacing-09);
  margin: 0;
  font-size: var(--text-2xl);

  @media (min-width: 768px) {
    font-size: var(--text-3xl);
    grid-column-start: first-column;
    grid-column-end: fourth-column;
    grid-row-start: row1-start;
    grid-row-end: row1-end;
    padding-bottom: 0;
    padding-top: 0;
  }

  @media (min-width: 1024px) {
    grid-column-end: fourth-column;
  }

  @media (min-width: 1224px) {
    font-size: var(--text-5xl);
  }
`;
const BoxText = styled.span`
  display: block;
  padding-bottom: var(--spacing-06);

  @media (min-width: 768px) {
    grid-column-start: first-column;
    grid-column-end: fourth-column;
    grid-row-start: row1-end;
    grid-row-end: third-line;
    align-self: start;
    padding-bottom: 0;
  }

  @media (min-width: 1024px) {
    grid-column-end: between-column;
  }
`;
const ButtonAnchorInfoBox = styled(ButtonAnchor)`
  grid-column-start: first-column;
  grid-column-end: span second-column;
  grid-row-start: third-line;
  grid-row-end: fourth-line;
  align-self: start;
  justify-self: start;
`;

export default function InfoBox() {
  return (
    <Box>
      <InnerBox>
        <BoxHeadline>{t("InfoBox.heading")}</BoxHeadline>
        <BoxText>{t("InfoBox.text")}</BoxText>
        <ButtonAnchorInfoBox url={anchorRegister.url}>
          {anchorRegister.text}
        </ButtonAnchorInfoBox>
        <Picture>
          <source
            media="(min-width: 1224px)"
            srcSet="../images/InfoBox-Image-L.png"
          />
          <source
            media="(min-width: 1024px)"
            srcSet="../images/InfoBox-Image-M.png"
          />
          <source
            media="(min-width: 768px)"
            srcSet="../images/InfoBox-Image-S.png"
          />
          <source srcSet="../images/InfoBox-Image-XS.png" />
          <img src="../images/InfoBox-Image-S.png" alt="Tablets mit Webapp des Steuerlotsen" />
        </Picture>
      </InnerBox>
    </Box>
  );
}
