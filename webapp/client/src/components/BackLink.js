import PropTypes from "prop-types";
import styled from "styled-components";
import backArrow from "./../assets/icons/arrow_back.svg";

const Anchor = styled.a`
  font-weight: var(--font-bold);
  font-size: var(--text-sm);
  line-height: var(--lineheight-s);
  text-transform: uppercase;
  letter-spacing: var(--tracking-extra-wide);
  text-decoration: none !important;

  &:focus {
    text-decoration: none;
  }

  &:visited {
    color: var(--text-color);
  }

  &:focus &:active {
    color: var(--text-color);
    background-color: none;
  }
`;

const LinkElement = styled.span`
  color: var(--text-color);
  vertical-align: middle;
`;

const Icon = styled(LinkElement)`
  --size: var(--back-link-size);
  content: url(${backArrow});
  margin: 3px 3px 3px 0px;

  width: var(--size);
  height: var(--size);

  border-radius: 50%;
`;

export default function BackLink({ text, url }) {
  return (
    <Anchor href={url}>
      <Icon />
      <LinkElement>{text}</LinkElement>
    </Anchor>
  );
}

BackLink.propTypes = {
  text: PropTypes.string,
  url: PropTypes.string,
};
