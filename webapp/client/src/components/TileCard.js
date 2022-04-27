import PropTypes from "prop-types";
import styled from "styled-components";
import arrowRight from "../assets/icons/simple_arrow_right.svg";

const LinkCard = styled.a`
  background-color: white;
  display: block;
  color: var(--text-color);
  text-decoration: none !important;
  outline: none !important;
  text-align: center;
  height: 188px;

  &:visited,
  &:hover,
  &:active,
  &:focus {
    color: var(--text-color);
    text-decoration: none !important;
    outline: none !important;
  }
`;

const Card = styled.div`
  margin-bottom: var(--spacing-02);
  font-family: var(--font-bold);
`;

const Icon = styled.img`
  margin-top: var(--spacing-05);
  margin-bottom: var(--spacing-04);
`;

const IconArrow = styled.img`
  width: 1.2em;
  height: 1.2em;
`;

function TileCard({ title, icon, url }) {
  return (
    <LinkCard href={url}>
      <Icon src={icon} />
      <Card>{title}</Card>
      <IconArrow src={arrowRight} />
    </LinkCard>
  );
}

TileCard.propTypes = {
  title: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};

export default TileCard;
