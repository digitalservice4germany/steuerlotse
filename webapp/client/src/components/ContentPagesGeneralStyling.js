import styled from "styled-components";

export const ContentWrapper = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 var(--spacing-03);
  max-width: var(--main-max-width);

  @media (min-width: 1224px) {
    margin: 0 var(--spacing-12);
  }
`;

export const List = styled.ul`
  margin: 0;
  padding: var(--spacing-03) 0 0;
  font-size: var(--text-medium-big);
`;

export const AnchorListItem = styled.li`
  padding-bottom: var(--spacing-01);
  list-style: none;
`;

export const ListItem = styled.li`
  padding-bottom: var(--spacing-01);
  list-style-position: inside;
  padding-left: 1.28571429em;
  text-indent: -1.28571429em;
`;

export const Headline1 = styled.h1`
  margin: 0;
  padding-bottom: var(--spacing-03);
  font-size: var(--text-3xl);

  @media (min-width: 768px) {
    font-size: var(--text-4xl);
  }
`;

export const Headline2 = styled.h2`
  padding-top: var(--spacing-09);
  margin: 0;
  font-size: var(--text-2xl);

  @media (min-width: 768px) {
    font-size: var(--text-3xl);
  }
`;

export const Paragraph = styled.p`
  padding-top: var(--spacing-03);
  margin: 0;
  font-size: var(--text-medium-big);
`;

export const ParagraphLarge = styled(Paragraph)`
  @media (min-width: 768px) {
    font-size: var(--text-2xl);
  }
`;

export default {
  ContentWrapper,
  List,
  AnchorListItem,
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
  ParagraphLarge,
};
