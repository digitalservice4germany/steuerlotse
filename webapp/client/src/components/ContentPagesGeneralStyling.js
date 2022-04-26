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

  @media (max-width: 425px) {
    font-size: var(--text-3xl);
  }
`;

export const Headline2 = styled(Headline1)`
  font-size: var(--text-3xl);

  @media (max-width: 768px) {
    font-size: var(--text-2xl);
  }
  @media (max-width: 425px) {
    font-size: var(--text-medium-big);
  }
`;

export const Paragraph = styled.p`
  padding-bottom: ${(props) =>
    props.spacingVariant ? 0 : "var(--spacing-09)"};
  margin: 0;
  margin-bottom: ${(props) =>
    !props.spacingVariant ? 0 : "var(--spacing-03)"};
  font-size: ${(props) =>
    props.textSizeVariant ? "var(--text-2xl)" : "var(--text-medium-big)"};
  max-width: ${(props) => (props.textSizeVariant ? "780px" : "730px")};
  line-height: 158%;
  @media (max-width: 425px) {
    font-size: var(--text-medium-big);
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
};
