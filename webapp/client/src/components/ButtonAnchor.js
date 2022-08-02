import PropTypes from "prop-types";
import styled, { css } from "styled-components";
import addPlausibleGoal from "../lib/helpers";
import { ReactComponent as PlayIcon } from "../assets/icons/play_icon.svg";

const hoverStates = css`
  color: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "var(--button-disabled-outline-font-color)";
    }
    if (variant === "outline") {
      return "var(--text-color)";
    }
    return "var(--inverse-text-color)";
  }};
  background-color: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "var(--button-disabled-outline-bg-color)";
    }
    if (variant === "outline") {
      return "var(--inverse-text-color)";
    }
    if (disabled) {
      return "var(--button-disabled-bg-color)";
    }
    return "var(--link-hover-color)";
  }};
  border: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "1px solid var(--button-outline-color)";
    }
    if (variant === "outline") {
      return "1px solid var(--hover-border-color)";
    }
    return "none";
  }};
  text-decoration: none;

  .anchor-btn__icon.translate-x {
    transform: translatex(10%);
  }
`;
const focusVisibleStates = css`
  color: var(--focus-text-color) !important;
  outline: none;
  box-shadow: none;
  background: linear-gradient(
    var(--focus-color) calc(100% - 4px),
    var(--focus-text-color) 4px
  );

  svg {
    path {
      fill: var(--focus-text-color);
    }
  }
`;
const activeStates = css`
  color: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "var(--button-disabled-outline-font-color)";
    }
    if (variant === "outline") {
      return "var(--text-color)";
    }
    return "var(--inverse-text-color)";
  }};
  background-color: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "var(--button-disabled-outline-bg-color)";
    }
    if (variant === "outline") {
      return "var(--inverse-text-color)";
    }
    if (disabled) {
      return "var(--button-disabled-bg-color)";
    }
    return "var(--button-primary-pressed-bg-color)";
  }};
  border: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "1px solid var(--button-outline-color)";
    }
    if (variant === "outline") {
      return "1px solid var(--hover-border-color)";
    }
    return "none";
  }};
`;

const Button = styled.button`
  box-sizing: border-box;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: ${(props) => props.marginVariant && "var(--spacing-03)"};
  margin-top: ${(props) => props.marginTop && "var(--spacing-03)"};
  font-size: var(--text-medium);
  font-family: var(--font-bold);
  line-height: 1;
  text-decoration: none;
  border: transparent;
  height: ${({ buttonStyle }) => {
    if (buttonStyle === "narrow") {
      return "var(--button-height-narrow)";
    }
    return "var(--button-height)";
  }};
  padding: ${({ buttonStyle }) => {
    if (buttonStyle === "narrow") {
      return "10px 12px";
    }
    return "18px 20px";
  }};
  color: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "var(--button-disabled-outline-font-color)";
    }
    if (variant === "outline") {
      return "var(--text-color)";
    }
    return "var(--inverse-text-color) !important"; // remove if possible
  }};
  background-color: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "var(--button-disabled-outline-bg-color)";
    }
    if (variant === "outline") {
      return "var(--inverse-text-color)";
    }
    if (disabled) {
      return "var(--button-disabled-bg-color)";
    }
    return "var(--link-color)";
  }};
  border: ${({ variant, disabled }) => {
    if (disabled && variant === "outline") {
      return "1px solid var(--button-outline-color)";
    }
    if (variant === "outline") {
      return "1px solid var(--border-color)";
    }
    return "none";
  }};

  &:hover {
    ${hoverStates};
  }

  &:focus-visible {
    ${focusVisibleStates};
  }

  &:active {
    ${activeStates};
  }

  &:focus {
    outline: none;
  }
`;
const AnchorButtonText = styled.span`
  padding: 0 4px;
`;
const AnchorButtonIcon = styled.span`
  padding: 0 4px;

  svg {
    display: block;
    margin: auto;
    max-height: 36px;
    max-width: 36px;
  }
`;

const ButtonAnchorForPlayer = styled(Button)`
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

function Text({ children }) {
  return (
    <AnchorButtonText className="anchor-btn__text">{children}</AnchorButtonText>
  );
}

Text.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
};

function Icon({ children, hoverVariant }) {
  const iconClasses = `anchor-btn__icon ${hoverVariant}`;

  return (
    <AnchorButtonIcon className={iconClasses}>{children}</AnchorButtonIcon>
  );
}

Icon.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
  hoverVariant: PropTypes.oneOf(["translate-x"]),
};
Icon.defaultProps = {
  hoverVariant: null,
};

export default function ButtonAnchor({
  children,
  onClick,
  url,
  name,
  download,
  variant,
  buttonStyle,
  external,
  disabled,
  className,
  marginVariant,
  plausibleGoal,
  plausibleDomain,
  plausibleProps,
  marginTop,
  isExternalLink,
  text,
}) {
  const handleClick = () => {
    if (plausibleDomain) {
      let props;

      if (plausibleProps.props === undefined) {
        props = {
          props: plausibleProps,
        };
      } else {
        props = plausibleProps;
      }

      addPlausibleGoal(plausibleDomain, plausibleGoal, props);
    }
    if (onClick !== undefined) {
      onClick();
    }
  };
  const relation = [];
  let target = false;
  if (external) {
    target = "_blank";
    relation.push("noopener");
  }

  const isUrl = () => {
    if (url) {
      return "a";
    }
    return "button";
  };

  const isDisabled = () => {
    if (!url) {
      return disabled;
    }
    return undefined;
  };

  const rel = () => {
    if (url && !download) {
      return relation;
    }
    return undefined;
  };

  return !isExternalLink ? (
    <Button
      as={isUrl()}
      className={className}
      href={url}
      variant={variant}
      disabled={isDisabled()}
      name={name}
      download={download}
      external={external}
      buttonStyle={buttonStyle}
      target={target || undefined}
      rel={rel()}
      onClick={handleClick}
      marginVariant={marginVariant}
      marginTop={marginTop}
    >
      {children}
    </Button>
  ) : (
    <ButtonAnchorForPlayer
      as={isUrl()}
      href={url}
      name={name}
      onClick={handleClick}
      target="_blank"
      rel="noopener"
    >
      <PlayIcon />
      {text}
    </ButtonAnchorForPlayer>
  );
}

ButtonAnchor.Text = Text;
ButtonAnchor.Icon = Icon;

ButtonAnchor.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
  onClick: PropTypes.func,
  url: PropTypes.string,
  name: PropTypes.string,
  download: PropTypes.bool,
  external: PropTypes.bool,
  buttonStyle: PropTypes.oneOf(["default", "narrow"]),
  variant: PropTypes.oneOf(["primary", "outline"]),
  disabled: PropTypes.bool,
  className: PropTypes.string,
  marginVariant: PropTypes.bool,
  marginTop: PropTypes.bool,
  plausibleGoal: PropTypes.string,
  plausibleProps: PropTypes.shape({
    method: PropTypes.string,
    props: PropTypes.any,
  }),
  plausibleDomain: PropTypes.string,
  isExternalLink: PropTypes.bool,
  text: PropTypes.string,
};

ButtonAnchor.defaultProps = {
  url: undefined,
  onClick: undefined,
  name: undefined,
  download: false,
  external: false,
  variant: "primary",
  buttonStyle: "default",
  disabled: false,
  className: undefined,
  marginVariant: false,
  marginTop: false,
  plausibleGoal: null,
  plausibleProps: undefined,
  plausibleDomain: null,
  isExternalLink: false,
  text: null,
};
