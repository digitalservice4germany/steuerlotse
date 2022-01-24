import PropTypes from "prop-types";
import styled from "styled-components";
import { ReactComponent as BackArrow } from "../assets/icons/arrow_back.svg";

const Anchor = styled.a`
  display: inline-flex;
  align-items: center;
  font-weight: var(--font-bold);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: var(--tracking-extra-wide);
  text-decoration: none;
  padding-top: 0.3rem;

  > svg {
    margin-right: 5px;
  }

  &:focus {
    span:last-child {
      background-color: var(--focus-color);
      border-bottom: 1px solid var(--text-color);
    }

    > svg {
      circle {
        fill: var(--focus-color);
      }
    }
  }

  &:hover {
    text-decoration: none;

    > svg {
      circle {
        fill: var(--icon-hover-color);
      }
    }
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
  border-bottom: 1px solid transparent;
  padding: 3px 3px 0;
`;

export default function BackLink({ text, url }) {
  return (
    <Anchor href={url}>
      <BackArrow />
      <LinkElement>{text}</LinkElement>
    </Anchor>
  );
}

BackLink.propTypes = {
  text: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};
