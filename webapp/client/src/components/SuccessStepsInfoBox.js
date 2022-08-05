import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";
import AnchorButton from "./AnchorButton";
import ShareButtons from "./ShareButtons";

const Box = styled.div`
  background-color: var(--white);
  display: flex;
  margin-top: ${(props) =>
    props.shareBoxSpacingVariant
      ? "calc(var(--spacing-09) + 4px)"
      : "var(--spacing-03)"};
  margin-bottom: ${(props) =>
    props.shareBoxSpacingVariant && "calc(var(--spacing-09) + 4px)"};
  border: 1px solid var(--beige-300);

  @media (max-width: 576px) {
    flex-direction: column;
    margin-top: ${(props) =>
      props.shareBoxSpacingVariant ? "var(--spacing-08)" : "var(--spacing-03)"};
    margin-bottom: ${(props) =>
      props.shareBoxSpacingVariant && "var(--spacing-08)"};
    border: 1px solid var(--beige-300);
  }
`;

const InnerBox = styled.div`
  padding: ${(props) =>
    props.className ? "32px 64px 48px 30px" : "32px 152px 48px 48px"};
  padding-bottom: ${(props) => props.textOnly && "32px"};

  padding-bottom: ${(props) => props.shareBoxSpacingVariant && "40px"};
  padding-right: ${(props) => props.shareBoxSpacingVariant && "131px"};

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
  @media (max-width: 568px) {
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

    @media (max-width: 576px) {
      width: 100%;
    }
  }
`;

export default function SuccessStepsInfoBox({
  header,
  text,
  anchor,
  image,
  icon,
  plausibleDomain,
  plausibleGoal,
  plausiblePropsButton,
  promoteUrl,
  shareText,
  mailSubject,
  sourcePage,
  shareBoxSpacingVariant,
  textOnly,
  imageDescription,
}) {
  return (
    <Box shareBoxSpacingVariant={shareBoxSpacingVariant}>
      {icon && <Icon src={icon.iconSrc} alt={icon.altText} />}
      <InnerBox
        className={icon}
        textOnly={textOnly}
        shareBoxSpacingVariant={shareBoxSpacingVariant}
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
              <source
                media="(min-width: 1024px)"
                srcSet={image.srcSetLargeScreen}
              />
              <source
                media="(max-width: 1024px)"
                srcSet={image.srcSetSmallerScreen}
              />
              <img src={image.src} alt={image.alt} />
            </picture>
            {imageDescription && (
              <InnerBoxText>{imageDescription}</InnerBoxText>
            )}
          </Figure>
        )}
        {shareText && (
          <ShareButtons
            header={header}
            text={text}
            shareText={shareText}
            mailSubject={mailSubject}
            sourcePage={sourcePage}
            plausibleDomain={plausibleDomain}
            promoteUrl={promoteUrl}
            variant
          />
        )}
      </InnerBox>
    </Box>
  );
}

SuccessStepsInfoBox.propTypes = {
  header: PropTypes.string,
  text: PropTypes.string,
  image: PropTypes.shape({
    src: PropTypes.string,
    srcSetLargeScreen: PropTypes.string,
    srcSetSmallerScreen: PropTypes.string,
    alt: PropTypes.string,
  }),
  anchor: PropTypes.shape({
    url: PropTypes.string,
    text: PropTypes.string,
  }),
  icon: PropTypes.string,
  plausibleDomain: PropTypes.string,
  plausibleGoal: PropTypes.string,
  plausiblePropsButton: PropTypes.shape({ method: PropTypes.string }),
  promoteUrl: PropTypes.string,
  shareText: PropTypes.string,
  mailSubject: PropTypes.string,
  sourcePage: PropTypes.string,
  shareBoxSpacingVariant: PropTypes.bool,
  textOnly: PropTypes.bool,
  imageDescription: PropTypes.string,
};

SuccessStepsInfoBox.defaultProps = {
  plausibleDomain: null,
  plausibleGoal: null,
  plausiblePropsButton: null,
  header: null,
  text: null,
  image: null,
  anchor: null,
  icon: null,
  promoteUrl: null,
  shareText: null,
  mailSubject: null,
  sourcePage: null,
  shareBoxSpacingVariant: false,
  textOnly: false,
  imageDescription: null,
};
