import styled from "styled-components";

export const ContentWrapper = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 auto;
  max-width: var(--main-max-width);
`;
export const List = styled.ul`
  margin: 0;
  padding: 0 0 var(--spacing-09) 0;
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
  padding-bottom: var(--spacing-06);
  margin: 0;
`;

export const Headline2 = styled(Headline1)``;

export const Paragraph = styled.p`
  padding-bottom: var(--spacing-09);
  margin: 0;
`;

export default {
  ContentWrapper,
  List,
  AnchorListItem,
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
};
