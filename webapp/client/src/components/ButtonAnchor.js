import PropTypes from "prop-types";
import styled, { css } from "styled-components";

const activeStates = css`
  &:active {
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
        return "1px solid var(--button-disabled-outline-color)";
      }
      if (variant === "outline") {
        return "1px solid var(--hover-border-color)";
      }
      return "none";
    }};
  }
`;

const Button = styled.button`
   {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: var(--text-medium);
    font-family: var(--font-bold);
    line-height: 1;
    text-decoration: none;
    border: transparent;
    transition: color var(--transition-behaviour) var(--transition-time),
      background-color var(--transition-behaviour) var(--transition-time),
      background var(--transition-behaviour) var(--transition-time);
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
        return "1px solid var(--button-disabled-outline-color)";
      }
      if (variant === "outline") {
        return "1px solid var(--border-color)";
      }
      return "none";
    }};

    &:hover {
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
          return "1px solid var(--button-disabled-outline-color)";
        }
        if (variant === "outline") {
          return "1px solid var(--hover-border-color)";
        }
        return "none";
      }};
      text-decoration: none;

      ${activeStates};

      .anchor-btn__icon.translate-x {
        transform: translatex(10%);
      }
    }

    ${activeStates};

    &:focus-visible {
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
    }
  }
`;
const AnchorButtonText = styled.span`
   {
    padding: 0 4px;
  }
`;
const AnchorButtonIcon = styled.span`
   {
    padding: 0 4px;

    svg {
      display: block;
      margin: auto;
      max-height: 36px;
      max-width: 36px;
    }
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
}) {
  const relation = [];
  let target = false;
  if (external) {
    target = "_blank";
    relation.push("noopener");
  }

  return (
    <Button
      as={url ? "a" : ""}
      className={className}
      href={url}
      variant={variant}
      disabled={!url ? disabled : undefined}
      name={name}
      download={download}
      external={external}
      buttonStyle={buttonStyle}
      target={target || undefined}
      rel={url && !download ? relation : undefined}
      onClick={onClick}
    >
      {children}
    </Button>
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
};
