import styled from "styled-components";

export const ContentTopSpacing = styled.div`
  margin-top: 9.375rem;
  position: relative;

  & img {
    width: 930px;

    @media (max-width: 1280px) {
      width: 843px;
    }
    @media (max-width: 1024px) {
      width: 813px;
    }

    @media (max-width: 768px) {
      width: 728px;
    }
    @media (max-width: 735px) {
      width: 700px;
    }
    @media (max-width: 600px) {
      width: 660px;
    }
    @media (max-width: 475px) {
      width: 611px;
    }
    @media (max-width: 425px) {
      width: 320px;
    }
  }
`;
export const HeadingText = styled.h1`
  font-size: 2.25rem;
  width: 832px;
  @media (max-width: 1024px) {
    width: 811px;
  }
  @media (max-width: 768px) {
    width: 636px;
  }
  @media (max-width: 425px) {
    width: 320px;
  }
  @media (max-width: 320px) {
    font-size: 2.25rem;
  }
`;
export const ParagraphIntroText = styled.p`
  font-size: 1.75rem;
  width: 832px;
  @media (max-width: 1024px) {
    width: 811px;
  }
  @media (max-width: 768px) {
    width: 636px;
  }
  @media (max-width: 425px) {
    width: 320px;
    font-size: 1.5rem;
  }
`;
export const ContentText = styled.div`
  width: fit-content;
`;
export const ParagraphTextLarger = styled.p`
  font-size: 1.5rem;
  width: 738px;

  @media (max-width: 768px) {
    font-size: 1.25rem;
    width: 600px;
  }

  @media (max-width: 425px) {
    font-size: 1.25rem;
    width: 320px;
  }
`;
export const ParagraphHeadingText = styled.p`
  font-size: var(--text-2xl);
  width: 738px;

  @media (max-width: 768px) {
    width: 600px;
  }

  @media (max-width: 425px) {
    font-size: 1.25rem;
    width: 320px;
  }
`;
export const ListBox = styled.div`
  background: var(--bg-highlight-color);
  padding: 32px;
  list-style-type: none;
  width: fit-content;

  @media (max-width: 425px) {
    width: 320px;
  }

  @media (max-width: 360px) {
    width: fit-content;
  }
`;
export const ListBoxText = styled(ParagraphTextLarger)`
  width: 668px;

  @media (max-width: 768px) {
    width: 536px;
  }

  @media (max-width: 425px) {
    width: 100%;
  }
`;
export const QuestionBoxBackground = styled.div`
  background: var(--bg-highlight-color);
  height: 459px;
  width: calc(100vw - 220px);
  position: relative;
  left: calc(-50vw + 82%);
  display: flex;
  justify-content: center;
  margin-bottom: -92px;

  @media (max-width: 1042px) {
    left: calc(-50vw + 85.2%);
  }

  @media (max-width: 1024px) {
    left: -1.75rem;
    width: 100vw;
  }

  @media (max-width: 900px) {
    left: -1rem;
    width: 100vw;
    margin-top: 5rem;
  }

  @media (max-width: 600px) {
    width: 700px;
  }

  @media (max-width: 425px) {
    height: 615px;
    width: 100vw;
  }
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

export default {
  ContentTopSpacing,
  HeadingText,
  ParagraphIntroText,
  ContentText,
  ParagraphTextLarger,
  ParagraphHeadingText,
  ListBox,
  ListBoxText,
  QuestionBoxBackground,
  QuestionBoxLayer,
  QuestionBox,
  ParagraphTextMedium,
  QuestionBoxAnchorButtons,
};
