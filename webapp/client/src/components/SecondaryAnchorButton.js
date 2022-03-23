import PropTypes from "prop-types";
import styled from "styled-components";
import addPlausibleGoal from "../lib/helpers";

const AnchorSecondary = styled.a`
  padding: 18px 24px 18px 24px;
  font-size: var(--text-base);
  font-weight: var(--font-bold);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;
  color: var(--text-color);
  width: fit-content;

  margin-right: var(--spacing-05);

  background: white;
  background-clip: padding-box;

  border: 0;
  border-radius: 0;
  border: 1px solid var(--border-color);

  &:not(:disabled):not(.disabled):active {
    color: var(--link-active-color);
    background-color: inherit;
    border: 1px solid var(--link-active-color);
  }

  &:hover {
    color: var(--link-hover-color);
    border: 1px solid var(--link-hover-color);

    background: var(--link-hover-color);
    border: none;
    border-bottom: 4px solid var(--link-hover-color);
    color: var(--inverse-text-color);
    text-decoration: none;
  }

  &:focus {
    color: var(--focus-text-color);
    background: var(--focus-color);
    outline: none;
    box-shadow: none;
    border: 0;
    border-bottom: 4px solid var(--focus-border-color);
  }
`;

export default function SecondaryAnchorButton({
  text,
  url,
  name,
  isDownloadLink,
  plausibleName,
  plausibleDomain,
  className,
}) {
  const onClickPlausible = () => {
    addPlausibleGoal(plausibleDomain, plausibleName);
  };
  return (
    <AnchorSecondary
      href={url}
      download={isDownloadLink}
      name={name}
      onClick={onClickPlausible}
      className={className}
    >
      {text}
    </AnchorSecondary>
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
};

SecondaryAnchorButton.defaultProps = {
  name: undefined,
  isDownloadLink: false,
  plausibleName: null,
  className: undefined,
  plausibleDomain: null,
};
