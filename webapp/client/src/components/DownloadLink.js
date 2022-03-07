import PropTypes from "prop-types";
import styled from "styled-components";
import { ReactComponent as DownloadIcon } from "../assets/icons/download_icon.svg";

const Anchor = styled.a`
  --total-line-height: var(--lineheight-l);
  --font-size: var(--text-base);
  position: relative;
  font-weight: var(--font-bold);
  font-size: var(--font-size);
  line-height: var(--total-line-height);

  ${({ large }) =>
    large &&
    `
        --adjust-position: -0.2;
        --margin-right: 14px;
        --font-size: var(--text-xl);
    `}
`;

const LinkElement = styled.span`
  --total-line-height: var(--lineheight-l);
  --size: 1.6em;
  --adjust-position: -0.4;
  --margin-right: 6px;
  content: "";
  display: inline-block;
  margin: 0 var(--margin-right) calc(var(--adjust-position) * var(--size)) 0;
  top: 0;

  line-height: var(--total-line-height);
  width: var(--size);
  height: var(--size);

  text-align: center;
  font-weight: var(--font-bold);
  color: var(--text-color);
  border-radius: 50%;
`;

export default function DownloadLink({ text, url, large }) {
  return (
    <Anchor large={large} href={url}>
      <LinkElement large={large}>
        <DownloadIcon />
      </LinkElement>
      {text}
    </Anchor>
  );
}

DownloadLink.propTypes = {
  text: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  large: PropTypes.bool,
};

DownloadLink.defaultProps = {
  large: false,
};
