import styled from "styled-components";

export const ContentSpacingWrapper = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  max-width: var(--pages-max-width);

  @media (min-width: 769px) {
    padding-left: var(--spacing-10);
    padding-right: var(--spacing-10);
  }

  @media (min-width: 1280px) {
    padding-left: var(--spacing-12);
    padding-right: var(--spacing-03);
  }
`;
export const IntroHeadingText = styled.h1`
  font-size: var(--text-4xl);
`;
export const IntroParagraphText = styled.p`
  font-size: 1.75rem;

  @media (max-width: 576px) {
    font-size: 1.5rem;
  }
`;
export const ContentText = styled.div`
  max-width: 738px;

  @media (max-width: 768px) {
    max-width: 600px;
  }
`;
export const ParagraphTextLarger = styled.p`
  font-size: 1.5rem;

  @media (max-width: 576px) {
    font-size: 1.25rem;
  }
`;
export const ParagraphHeadingLarger = styled.p`
  font-size: var(--text-2xl);

  @media (max-width: 576px) {
    font-size: 1.25rem;
  }
`;
export const ListBox = styled.div`
  background: var(--bg-highlight-color);
  padding: 32px 36px 32px 32px;
  list-style-type: none;

  @media (max-width: 576px) {
    padding: 16px;
  }
`;

export const ListBoxText = styled(ParagraphTextLarger)``;

export const QuestionBoxBackground = styled.div`
  background: var(--bg-highlight-color);
  position: relative;
  display: flex;
  justify-content: center;
`;
export const QuestionBoxLayer = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: auto;
  flex: 1;
  width: 100%;
  max-width: var(--main-max-width);
`;
export const QuestionBox = styled.div`
  padding: 50px 0;
`;
export const ParagraphTextMedium = styled.p`
  font-size: 1.25rem;
`;
export const QuestionBoxAnchorButtons = styled.div`
  @media (max-width: 605px) {
    display: flex;
    flex-direction: column;
  }
`;
export const HeroImage = styled.img`
  max-width: 100%;
  padding-top: var(--spacing-08);
`;
export const ContentSection = styled.section`
  display: flex;
  flex-direction: column;
`;
export const TextContent = styled.p`
  font-size: 1.5rem;
  @media (max-width: 425px) {
    font-size: var(--text-xl);
  }
  @media (max-width: 375px) {
    font-size: 1.125rem;
  }
`;
export const ParagraphHeading = styled.h3`
  font-size: var(--text-2xl);
  padding-top: var(--spacing-08);
  font-family: var(--font-bold);

  @media (max-width: 425px) {
    font-size: var(--text-xl);
  }

  @media (max-width: 375px) {
    font-size: 1.25rem;
  }
`;

export const ShareBox = styled.div`
  max-width: 738px;
`;

export const Picture = styled.picture`
  img {
    width: 100%;
    max-width: 930px;
    height: auto;
    object-fit: contain;
  }
`;

export const HeaderSection = styled.div`
  margin-top: var(--spacing-11);

  @media (max-width: 768px) {
    margin-top: var(--spacing-09);
  }
`;

export const TopContent = styled.div`
  max-width: 832px;
  @media (max-width: 768px) {
    max-width: 636px;
  }
`;
