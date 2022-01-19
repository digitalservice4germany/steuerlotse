import PropTypes from "prop-types";
import styled from "styled-components";
import backArrow from "../assets/icons/arrow_back.svg";

const Anchor = styled.a`
  display: inline-flex;
  align-items: center;
  font-weight: var(--font-bold);
  font-size: var(--text-sm);
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
  }
`;

const LinkElement = styled.span`
  color: var(--text-color);
  line-height: var(--back-link-size);
`;

const Icon = styled(LinkElement)`
  --size: var(--back-link-size);
  content: url(${backArrow});
  margin-right: 8px;
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
  text: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};
