import PropTypes from "prop-types";
import styled from "styled-components";
import arrowRight from "../assets/icons/simple_arrow_right.svg";

const LinkCard = styled.a`
  display: block;
  background-color: white;
  color: var(--text-color);
  text-decoration: none !important;
  outline: none !important;
  text-align: center;
  height: 188px;
  min-width: 274px;

  &:visited,
  &:hover,
  &:active,
  &:focus {
    color: var(--text-color);
    text-decoration: none !important;
    outline: none !important;
  }

  width: 32%;

  @media screen and (max-width: 869px) {
    width: 49%;
  }

  @media screen and (max-width: 587px) {
    width: 100%;
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

function TileCard({ title, icon, url, className }) {
  return (
    <LinkCard className={className} href={url}>
      <Icon src={icon} />
      <Card>{title}</Card>
      <IconArrow src={arrowRight} />
    </LinkCard>
  );
}

TileCard.propTypes = {
  className: PropTypes.string,
  title: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};

TileCard.defaultProps = {
  className: "",
};

export default TileCard;
