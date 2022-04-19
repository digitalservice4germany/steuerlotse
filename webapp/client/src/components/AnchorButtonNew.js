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
    padding: 0 16px;
  }
`;

export default function AnchorButtonNew({
  children,
  onClick,
  url,
  name,
  download,
}) {
  return (
    <Anchor
      className="anchor-btn"
      href={url}
      name={name}
      download={download}
      onClick={onClick}
    >
      <AnchorButtonText className="anchor-btn__text">
        {children}
      </AnchorButtonText>
    </Anchor>
  );
}

AnchorButtonNew.propTypes = {
  children: PropTypes.elementType.isRequired,
  onClick: PropTypes.func,
  url: PropTypes.string.isRequired,
  name: PropTypes.string,
  download: PropTypes.bool,
};

AnchorButtonNew.defaultProps = {
  onClick: null,
  name: null,
  download: false,
};
