import styled from "styled-components";
import PropTypes from "prop-types";
import ButtonAnchor from "./ButtonAnchor";

const Box = styled.div`
  background-color: var(--beige-200);
  padding-top: var(--spacing-09);
  margin-top: var(--spacing-11);
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

  @media screen and (min-width: 1136px) {
    padding-left: 0;
    padding-right: 0;
  }
`;

const TextBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-bottom: var(--spacing-09);

  @media (min-width: 768px) {
    padding-bottom: 13rem;
    grid-column: 1 / 4;
    grid-row: 1;
  }

  @media (min-width: 1224px) {
    grid-column: 1 / 3;
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
const Figure = styled.figure`
  margin: 0;
  align-self: end;

  @media (min-width: 768px) {
    grid-column: 2 / -1;
    grid-row: 1;
  }

  img {
    width: 95%;
    height: auto;
    object-fit: contain;

    @media (min-width: 768px) {
      width: 85%;
    }
  }
`;

export default function InfoBox({ boxHeadline, boxText, anchor }) {
  return (
    <Box>
      <InnerBox>
        <TextBox className="info-box__text">
          <BoxHeadline>{boxHeadline}</BoxHeadline>
          <BoxText>{boxText}</BoxText>
          <ButtonAnchor url={anchor.url}>{anchor.text}</ButtonAnchor>
        </TextBox>
        <Figure className="info-box__figure">
          <img
            srcSet="../images/InfoBox-Image-XS.png 726w,
                                ../images/InfoBox-Image-S.png 794w,
      	                        ../images/InfoBox-Image-M.png 1060w,
      	                        ../images/InfoBox-Image-L.png 1224w"
            sizes="(min-width: 768px) 50vw, 100vw"
            src="../images/InfoBox-Image-XS.png"
            alt="Tablets mit Webapp des Steuerlotsen"
          />
        </Figure>
      </InnerBox>
    </Box>
  );
}

InfoBox.propTypes = {
  boxHeadline: PropTypes.string,
  boxText: PropTypes.string,
  anchor: {
    url: PropTypes.string,
    text: PropTypes.string,
  },
};

InfoBox.defaultProps = {
  boxHeadline: null,
  boxText: null,
  anchor: {
    url: null,
    text: null,
  },
};
