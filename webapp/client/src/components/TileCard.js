import PropTypes from "prop-types";
import styled from "styled-components";
import arrowRight from "../assets/icons/simple_arrow_right.svg";

const LinkCard = styled.a`
  display: block;
  background-color: white;
  color: var(--text-color);
  text-decoration: none !important;
  text-align: center;
  height: 188px;
  min-width: 274px;

  &:visited,
  &:hover,
  &:active,
  &:focus {
    color: var(--text-color);
    text-decoration: none !important;
  }

  &:hover {
    .bounce {
      animation-duration: 1s;
      animation-iteration-count: 1;
      animation-name: bounce;
      animation-timing-function: ease;
    }
  }

  @keyframes bounce {
    0% {
      transform: translateX(0);
    }
    33% {
      transform: translateX(-10px);
    }
    66% {
      transform: translateX(10px);
    }
    100% {
      transform: translateX(0);
    }
  }
`;

const Card = styled.div`
  margin-bottom: var(--spacing-02);
  font-family: var(--font-bold);
`;

const Icon = styled.img`
  height: 50px;
  width: 52px;
  margin-top: var(--spacing-05);
  margin-bottom: var(--spacing-04);
`;

const IconArrow = styled.img`
  width: 1.2em;
  height: 1.2em;
`;

function TileCard({ title, icon, url, className, animateArrow }) {
  return (
    <LinkCard className={`${className} tile-card`} href={url}>
      <Icon src={icon} />
      <Card>{title}</Card>
      <IconArrow className={animateArrow ? "bounce" : ""} src={arrowRight} />
    </LinkCard>
  );
}

TileCard.propTypes = {
  className: PropTypes.string,
  title: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  animateArrow: PropTypes.bool,
};

TileCard.defaultProps = {
  className: "",
  animateArrow: true,
};

export default TileCard;
