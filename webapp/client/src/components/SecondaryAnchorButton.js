import PropTypes from "prop-types";
import styled from "styled-components";
import addPlausibleGoal from "../lib/helpers";
import { ReactComponent as DefaultStatePlayIcon } from "../assets/icons/DefaultStatePlayIcon.svg";
import { ReactComponent as PlayIcon } from "../assets/icons/play_icon.svg";

const AnchorSecondary = styled.a`
  padding: 18px 24px 18px 24px;
  font-size: var(--text-base);
  font-family: var(--font-bold);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;
  color: var(--text-color);
  width: fit-content;
  outline: 1px solid var(--border-color);
  margin-right: var(--spacing-05);
  background: white;
  background-clip: padding-box;
  border: 0;
  border-radius: 0;

  &:not(:disabled):not(.disabled):active {
    color: var(--inverse-text-color);
    background-color: var(--link-color);
    outline: 0;
    border-bottom: 4px solid var(--link-color);
  }

  &:hover {
    outline: 1px solid var(--link-hover-color);
    background: var(--link-hover-color);
    border: none;
    border-bottom: 4px solid var(--link-hover-color);
    color: var(--inverse-text-color);
    text-decoration: none;
  }

  &:focus-visible {
    color: var(--focus-text-color);
    background: var(--focus-color);
    outline: none;
    box-shadow: none;
    border: 0;
    border-bottom: 4px solid var(--focus-border-color);
  }
`;

const AnchorSecondaryPlayer = styled(AnchorSecondary)`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  font-size: var(--text-medium);
  outline: 0;
  display: flex;
  justify-content: space-between;
  width: 269px;

  @media (max-width: 425px) {
    font-size: var(--text-base);
    padding: 14px 18px 14px 18px;
    width: 240px;
  }
`;

const IconDefault = styled.div`
  position: absolute;
  top: -10%;

  @media (max-width: 425px) {
    top: -25%;
  }

  ${AnchorSecondaryPlayer}:hover & {
    display: none;
  }

  ${AnchorSecondaryPlayer}:active & {
    display: none;
  }
`;

const IconHover = styled.div`
  position: absolute;
  display: none;
  top: -10%;

  ${AnchorSecondaryPlayer}:hover & {
    display: block;
  }
`;

const Div = styled.div`
  position: relative;
`;

export default function SecondaryAnchorButton({
  text,
  url,
  name,
  isDownloadLink,
  plausibleName,
  plausibleDomain,
  className,
  isExternalLink,
}) {
  const handleClick = () => {
    addPlausibleGoal(plausibleDomain, plausibleName);
  };

  return !isExternalLink ? (
    <AnchorSecondary
      href={url}
      download={isDownloadLink}
      name={name}
      onClick={handleClick}
      className={className}
    >
      {text}
    </AnchorSecondary>
  ) : (
    <AnchorSecondaryPlayer
      href={url}
      name={name}
      onClick={handleClick}
      className={className}
      target="_blank"
      rel="noopener"
    >
      <Div className="mr-3">
        <IconDefault>
          <DefaultStatePlayIcon className="mr-3" />
        </IconDefault>
        <IconHover>
          <PlayIcon className="mr-3" />
        </IconHover>
      </Div>
      {text}
    </AnchorSecondaryPlayer>
  );
}

SecondaryAnchorButton.propTypes = {
  text: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  name: PropTypes.string,
  isDownloadLink: PropTypes.bool,
  plausibleName: PropTypes.string,
  className: PropTypes.string,
  plausibleDomain: PropTypes.string,
  isExternalLink: PropTypes.bool,
};

SecondaryAnchorButton.defaultProps = {
  name: undefined,
  isDownloadLink: false,
  plausibleName: null,
  className: undefined,
  plausibleDomain: null,
  isExternalLink: false,
};
