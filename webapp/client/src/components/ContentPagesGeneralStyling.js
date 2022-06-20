import styled from "styled-components";

export const ContentWrapper = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  max-width: var(--pages-max-width);

  margin-bottom: var(--spacing-10);

  @media (min-width: 769px) {
    padding-left: var(--spacing-06);
    padding-right: var(--spacing-06);
  }

  @media (min-width: 1280px) {
    padding-left: var(--spacing-12);
  }
`;

export const List = styled.ul`
  margin: 0;
  padding: var(--spacing-03) 0 0;
  font-size: var(--text-medium);
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
  margin-top: var(--spacing-11);
  padding-bottom: var(--spacing-03);
  font-size: var(--text-4xl);

  @media (max-width: 575px) {
    font-size: var(--text-3xl);
  }

  .header-navigation,
  .header-navigation + & {
    margin-top: var(--spacing-07);
  }

  @media (max-width: 1024px) {
    margin-top: var(--spacing-09);

    .header-navigation,
    .header-navigation + & {
      margin-top: var(--spacing-01);
    }
  }
`;

export const Headline2 = styled.h2`
  padding-top: var(--spacing-09);
  margin: 0;
  margin-bottom: ${(props) => props.marginVariant && "var(--spacing-03)"};
  font-size: var(--text-3xl);

  @media (max-width: 575px) {
    font-size: var(--text-xla);
  }
`;

export const Paragraph = styled.p`
  padding-top: ${(props) =>
    props.spacingVariant ? "var(--spacing-08)" : "var(--spacing-03)"};
  margin: 0;
  font-size: var(--text-medium);
  white-space: pre-line;
  line-height: var(--lineheight-l);
  letter-spacing: var(--tracking-normal);
`;

export const ParagraphLarge = styled(Paragraph)`
  @media (min-width: 768px) {
    font-size: var(--text-2xl);
  }
`;
