import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";
import AnchorButton from "./AnchorButton";

const Box = styled.div`
  background-color: var(--white);
  display: flex;
  margin-top: var(--spacing-03);
  border: 1px solid var(--beige-300);
`;

const Icon = styled.img`
  height: 50px;
  width: 50px;
  margin: 32px 0 0 48px;
`;

const InnerBoxHeader = styled.h2`
  font-size: var(--text-2xl);
  margin: 8px 0 6px;
`;

const InnerBoxText = styled.p`
  font-size: var(--text-medium);
  max-width: 657px;
  margin-top: var(--spacing-03);
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

export default function successStepsInfoBox({
  header,
  text,
  anchor,
  image,
  icon,
  plausibleDomain,
}) {
  const plausibleGoal = "Vorbereitungshilfe";
  const plausiblePropsButton = {
    method: "CTA Vorbereitungshilfe herunterladen",
  };

  return (
    <Box>
      {icon && <Icon src={icon} />}
      <div
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
        <Figure>{image && <img src={image.src} alt="exmaple" />}</Figure>
      </div>
    </Box>
  );
}

successStepsInfoBox.propTypes = {
  header: PropTypes.string,
  text: PropTypes.string,
  image: PropTypes.string,
  anchor: {
    url: PropTypes.string,
    text: PropTypes.string,
  },
  icon: PropTypes.string,
  plausibleDomain: PropTypes.string,
};

successStepsInfoBox.defaultProps = {
  plausibleDomain: null,
};
