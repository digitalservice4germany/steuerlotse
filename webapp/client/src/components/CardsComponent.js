import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import ArrowLeft from "../assets/icons/arrow_left.svg";

const Wrapper = styled.div`
  background-color: var(--bg-highlight-color);
  display: flex;
  padding: 3rem 2rem 0 2rem;
  gap: var(--spacing-06);

  @media (max-width: 767px) {
    flex-direction: column;
    padding: 0;
  }

  @media (max-width: 500px) {
    margin-top: var(--spacing-07);
  }
`;

const Card = styled.a`
  background-color: white;
  padding: var(--spacing-04);
  height: 100%;
  text-decoration: none;
  color: black;
  width: 33.33%;
  min-height: 450px;
  position: relative;

  @media (max-width: 767px) {
    width: 100%;
    min-height: 300px;
  }

  &:visited {
    color: inherit;
  }

  &:hover {
    text-decoration: none;
  }

  & h2 {
    font-size: 1.75rem;
    padding-bottom: 1rem;
  }

  & img {
    position: absolute;
    height: var(--spacing-08);
    width: var(--spacing-08);
    right: var(--spacing-04);
    bottom: var(--spacing-04);
  }
`;

export default function CardsComponent({ cards }) {
  return (
    <Wrapper>
      {cards.map((card, index) => [
        <Card href={card.url} key={index}>
          <h2>{card.header}</h2>
          <p>{card.text}</p>
          <img src={ArrowLeft} alt="arrow pointing left" />
        </Card>,
      ])}
    </Wrapper>
  );
}

CardsComponent.propTypes = {
  cards: PropTypes.arrayOf(
    PropTypes.shape({
      header: PropTypes.string,
      text: PropTypes.string,
      url: PropTypes.string,
    })
  ),
};

CardsComponent.defaultProps = {
  cards: {
    header: null,
    text: null,
    url: null,
  },
};
