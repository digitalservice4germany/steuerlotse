import styled from "styled-components";
import PropTypes from "prop-types";
import ButtonAnchor from "./ButtonAnchor";

const Box = styled.div`
  background-color: var(--beige-200);
  padding-top: var(--spacing-09);
  margin-top: var(--spacing-10);
`;
const InnerBox = styled.div`
  padding-left: var(--spacing-06);
  padding-right: var(--spacing-06);
  margin: 0 auto;
  max-width: var(--pages-max-width);
  display: flex;

  @media (max-width: 1024px) {
    padding-left: var(--spacing-06);
    padding-right: var(--spacing-06);
  }

  @media (max-width: 767px) {
    flex-direction: column;
    padding-left: var(--spacing-03);
    padding-right: var(--spacing-03);
  }
`;

const TextBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-bottom: var(--spacing-09);
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
  width: 100%;
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }

  @media (max-width: 767px) {
    align-self: center;
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
          <picture>
            <source
              media="(min-width: 1200px)"
              srcSet="../images/InfoBox-Image-L.png"
            />
            <source
              media="(min-width: 1024px)"
              srcSet="../images/InfoBox-Image-M.png"
            />
            <source
              media="(min-width: 798px)"
              srcSet="../images/InfoBox-Image-S.png"
            />
            <img
              src="../images/InfoBox-Image-XS.png"
              alt="Tablets mit Webapp des Steuerlotsen"
            />
          </picture>
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
