import PropTypes from "prop-types";
import styled from "styled-components";
import addPlausibleGoal from "../lib/helpers";

const Anchor = styled.a`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem;
  margin-right: var(--spacing-05);
  font-size: var(--text-base);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;
  color: var(--inverse-text-color);
  background: var(--link-color);
  display: inline-block;
  position: relative;
  border: none;
  border-radius: 0;
  border-bottom: 4px solid var(--link-color);

  &:not(:disabled):not(.disabled):active {
    background: var(--link-color) !important;
    border: none !important;
    border-bottom: 4px solid var(--link-color) !important;
  }

  &:hover {
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

  &:visited {
    color: var(--inverse-text-color);
  }
`;

const AnchorSecondary = styled.a`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem; /* The calculation subtracts the border-bottom height. We need a border-bottom for the focus state. */
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

export default function AnchorButton({
  text,
  url,
  name,
  isDownloadLink,
  isSecondaryButton,
  plausibleName,
  plausibleDomain,
  className,
}) {
  const onClickPlausible = () => {
    addPlausibleGoal(plausibleDomain, plausibleName);
  };
  return !isSecondaryButton ? (
    <Anchor
      href={url}
      download={isDownloadLink}
      name={name}
      onClick={onClickPlausible}
      className={className}
    >
      {text}
    </Anchor>
  ) : (
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

AnchorButton.propTypes = {
  text: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  name: PropTypes.string,
  isDownloadLink: PropTypes.bool,
  isSecondaryButton: PropTypes.bool,
  plausibleName: PropTypes.string,
  className: PropTypes.string,
  plausibleDomain: PropTypes.string,
};

AnchorButton.defaultProps = {
  name: undefined,
  isDownloadLink: false,
  isSecondaryButton: false,
  plausibleName: null,
  className: undefined,
  plausibleDomain: null,
};
