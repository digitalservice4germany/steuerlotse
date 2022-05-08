import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";
import AnchorButton from "./AnchorButton";

const Box = styled.div`
  background-color: var(--white);
  display: flex;
  margin-top: var(--spacing-03);
  border: 1px solid var(--beige-300);

  @media (max-width: 425px) {
    flex-direction: column;
    padding: 0 32px 32px;
  }

  @media (max-width: 360px) {
    padding: 0 16px 16px;
  }
`;

const InnerBox = styled.div``;

const InnerBoxHeader = styled.h2`
  font-size: var(--text-2xl);
  margin: 8px 0;

  @media (max-width: 425px) {
    margin-top: var(--spacing-03);
  }

  @media (max-width: 360px) {
    font-size: var(--text-medium-big);
  }
`;

const InnerBoxText = styled.p`
  font-size: var(--text-medium);
  margin-top: var(--spacing-03);
`;

const Icon = styled.img`
  height: 50px;
  width: 50px;
  margin: 32px 0 0 48px;

  @media (max-width: 768px) {
    margin-left: 33px;
  }

  @media (max-width: 425px) {
    margin-left: 0;
  }
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
    border: 1px solid var(--grey-100);

    @media (min-width: 768px) {
      width: 65%;
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
}) {
  return (
    <Box>
      {icon && <Icon src={icon} />}
      <InnerBox
        className={
          icon ? "steps_info_box_with_icon" : "steps_info_box_without_icon"
        }
      >
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
    sizes: PropTypes.string,
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
