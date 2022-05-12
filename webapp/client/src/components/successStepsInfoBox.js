import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";
import AnchorButton from "./AnchorButton";

const Box = styled.div`
  background-color: var(--white);
  display: flex;
  margin-top: var(--spacing-03);
  border: 1px solid var(--beige-300);

  @media (max-width: 576px) {
    flex-direction: column;
  }
`;

const InnerBox = styled.div`
  padding: ${(props) =>
    props.className ? "32px 64px 48px 30px" : "32px 152px 48px 48px"};
  padding-bottom: ${(props) => props.textOnly && "32px"};

  @media (max-width: 768px) {
    padding-right: 2.125rem;
    padding-bottom: ${(props) => (props.textOnly ? "1rem" : "2rem")};
    padding-top: 24px;
  }

  @media (max-width: 576px) {
    flex-direction: column;
    padding-top: ${(props) => (props.className ? "0.5rem" : "1.5rem")};
    padding-left: 2rem;
    padding-right: 2rem;
  }
`;

const InnerBoxHeader = styled.h3`
  font-size: var(--text-2xl);
  margin: 0.5rem 0;
`;

const InnerBoxText = styled.p`
  font-size: var(--text-medium);
  margin-top: var(--spacing-03);
`;

const Icon = styled.img`
  height: 50px;
  width: 50px;
  margin: 2rem 0 0 3rem;

  @media (max-width: 768px) {
    margin-left: 2rem;
  }
`;

const Figure = styled.figure`
  margin: 0;
  align-self: end;
  max-width: 658px;
  @media (min-width: 768px) {
    grid-column: 2 / -1;
    grid-row: 1;
  }

  img {
    width: 95%;
    height: auto;
    object-fit: contain;
    border: 1px solid var(--grey-100);

    @media (max-width: 768px) {
      width: 60%;
    }

    @media (max-width: 576px) {
      width: 100%;
    }
  }
`;

export default function successStepsInfoBox({
  header,
  text,
  anchor,
  image,
  icon,
  plausibleDomain,
  plausibleGoal,
  plausiblePropsButton,
  textOnly,
}) {
  return (
    <Box>
      {icon && <Icon src={icon.iconSrc} alt={icon.altText} />}
      <InnerBox className={icon} textOnly={textOnly}>
        <InnerBoxHeader>{header}</InnerBoxHeader>
        <InnerBoxText>{text}</InnerBoxText>
        {anchor && (
          <AnchorButton
            url={anchor.url}
            text={anchor.text}
            isDownloadLink
            plausibleDomain={plausibleDomain}
            plausibleGoal={plausibleGoal}
            plausibleProps={plausiblePropsButton}
          />
        )}
        {image && (
          <Figure>
            <picture>
              <img src={image.src} srcSet={image.srcSet} alt={image.alt} />
            </picture>
          </Figure>
        )}
      </InnerBox>
    </Box>
  );
}

successStepsInfoBox.propTypes = {
  header: PropTypes.string,
  text: PropTypes.string,
  image: {
    src: PropTypes.string,
    srcSet: PropTypes.string,
    alt: PropTypes.string,
  },
  anchor: {
    url: PropTypes.string,
  },
  icon: PropTypes.string,
  plausibleDomain: PropTypes.string,
  plausibleGoal: PropTypes.string,
  plausiblePropsButton: PropTypes.shape({ method: PropTypes.string }),
};

successStepsInfoBox.defaultProps = {
  plausibleDomain: null,
  plausibleGoal: null,
  plausiblePropsButton: null,
  header: null,
  text: null,
  image: null,
  anchor: null,
  icon: null,
};
