import PropTypes from "prop-types";
import styled from "styled-components";

const Anchor = styled.a`
   {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: var(--button-height);
    font-size: var(--text-medium);
    line-height: 1;
    letter-spacing: 0.01em;
    color: var(--inverse-text-color);
    background-color: var(--link-color);
    cursor: pointer;
    text-decoration: none;
    border: none;
    padding: 0;

    &.outline {
      color: var(--text-color);
      background-color: var(--inverse-text-color);
      border: 1px solid var(--border-color);
    }

    &:hover {
      color: var(--inverse-text-color);
      background-color: var(--link-hover-color);
      text-decoration: none;
    }

    &:focus-visible {
      color: var(--focus-text-color);
      outline: none;
      box-shadow: none;
      background: linear-gradient(
        var(--focus-color) calc(100% - 4px),
        var(--focus-text-color) 4px
      );
    }
  }
`;

const AnchorButtonText = styled.span`
   {
    padding: 0 24px;
  }
`;

const AnchorButtonIcon = styled.span`
   {
    padding: 12px 0 12px 24px;

    svg {
      display: block;
      margin: auto;
      height: 36px;
      width: 36px;
    }
  }
`;

export default function AnchorButtonNew({
  children,
  onClick,
  url,
  name,
  download,
  variant,
}) {
  return (
    <Anchor
      className={variant}
      href={url}
      name={name}
      download={download}
      onClick={onClick}
    >
      {children}
    </Anchor>
  );
}

AnchorButtonNew.propTypes = {
  children: PropTypes.elementType.isRequired,
  onClick: PropTypes.func,
  url: PropTypes.string.isRequired,
  name: PropTypes.string,
  download: PropTypes.bool,
  variant: PropTypes.string,
};

AnchorButtonNew.defaultProps = {
  onClick: null,
  name: null,
  download: false,
  variant: null,
};

function Text({ text }) {
  return (
    <AnchorButtonText className="anchor-btn__text">{text}</AnchorButtonText>
  );
}
Text.propTypes = {
  text: PropTypes.string.isRequired,
};
AnchorButtonNew.Text = Text;

function Icon({ children }) {
  return (
    <AnchorButtonIcon className="anchor-btn__icon">{children}</AnchorButtonIcon>
  );
}
Icon.propTypes = {
  children: PropTypes.elementType.isRequired,
};
AnchorButtonNew.Icon = Icon;
