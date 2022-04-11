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

  &:focus-visible {
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

export default function AnchorButton({
  text,
  url,
  name,
  isDownloadLink,
  plausibleGoal,
  plausibleDomain,
  plausibleProps,
  className,
}) {
  const handleClick = () => {
    addPlausibleGoal(plausibleDomain, plausibleGoal, { props: plausibleProps });
  };
  return (
    <Anchor
      href={url}
      download={isDownloadLink}
      name={name}
      onClick={handleClick}
      className={className}
    >
      {text}
    </Anchor>
  );
}

AnchorButton.propTypes = {
  text: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  name: PropTypes.string,
  isDownloadLink: PropTypes.bool,
  plausibleGoal: PropTypes.string,
  plausibleProps: PropTypes.shape({ method: PropTypes.string }),
  className: PropTypes.string,
  plausibleDomain: PropTypes.string,
};

AnchorButton.defaultProps = {
  name: undefined,
  isDownloadLink: false,
  plausibleGoal: null,
  plausibleProps: undefined,
  plausibleDomain: null,
  className: undefined,
};
