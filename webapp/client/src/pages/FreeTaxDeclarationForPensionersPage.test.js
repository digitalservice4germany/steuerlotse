import React from "react";
import { render, screen } from "@testing-library/react";
import FreeTaxDeclarationForPensionersPage from "./FreeTaxDeclarationForPensionersPage";
import i18n from "i18next";
import { I18nextProvider } from "react-i18next";

jest.mock("../components/ContentPageBox", () => ({
  __esModule: true,
  default: function ContentPageBox() {
    return <div>Content Page Box</div>;
  },
}));

jest.mock("../components/SuccessStepsInfoBox", () => ({
  __esModule: true,
  default: function SuccessStepsInfoBox() {
    return <div>Steps Info Box</div>;
  },
}));

const MOCK_PROPS = {
  plausibleDomain: "/plausibleDomain/path",
};

describe("FreeTaxDeclarationForPensionersPage translations", () => {
  const texts =
    i18n.getDataByLanguage("de").translation.freeTaxDeclarationForPensioners;
  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <FreeTaxDeclarationForPensionersPage {...MOCK_PROPS} />
      </I18nextProvider>
    );
  });

  it("should render heading", () => {
    expect(screen.getByText(texts.Heading)).toBeDefined();
  });

  it("should render teaser", () => {
    expect(screen.getByText(texts.Teaser)).toBeDefined();
  });

  it("should render anchor 1", () => {
    expect(screen.getByText(texts.AnchorList.anchor1)).toBeDefined();
  });

  it("should render anchor 2", () => {
    expect(screen.getByText(texts.AnchorList.anchor2)).toBeDefined();
  });

  it("should render anchor 3", () => {
    expect(screen.getByText(texts.AnchorList.anchor3)).toBeDefined();
  });

  it("should render accordion heading", () => {
    expect(screen.getByText(texts.Accordion.heading)).toBeDefined();
  });

  it("should render accordion item 1 heading", () => {
    expect(screen.getByText(texts.Accordion.Item1.heading)).toBeDefined();
  });

  it("should render accordion item 1 detail", () => {
    expect(screen.getByText(texts.Accordion.Item1.detail)).toBeDefined();
  });

  it("should render accordion item 2 heading", () => {
    expect(screen.getByText(texts.Accordion.Item2.heading)).toBeDefined();
  });

  it("should render accordion item 2 detail", () => {
    expect(screen.getByText(texts.Accordion.Item2.detail)).toBeDefined();
  });

  it("should render accordion item 3 heading", () => {
    expect(screen.getByText(texts.Accordion.Item3.heading)).toBeDefined();
  });

  it("should render accordion item 3 detail", () => {
    expect(screen.getByText(texts.Accordion.Item3.detail)).toBeDefined();
  });

  it("should render accordion item 4 heading", () => {
    expect(screen.getByText(texts.Accordion.Item4.heading)).toBeDefined();
  });

  it("should render accordion item 4 detail", () => {
    expect(screen.getByText(texts.Accordion.Item4.detail)).toBeDefined();
  });

  it("should render body part 1 heading", () => {
    expect(screen.getByText(texts.Body.part1.heading)).toBeDefined();
  });

  it("should render body part 1 subheading 1", () => {
    expect(screen.getByText(texts.Body.part1.subHeading1)).toBeDefined();
  });

  it("should render body part 1 text 1", () => {
    expect(screen.getByText(texts.Body.part1.text1)).toBeDefined();
  });

  it("should render body part 1 text 2", () => {
    expect(screen.getByText(texts.Body.part1.text2)).toBeDefined();
  });

  it("should render body part 1 subheading 2", () => {
    expect(screen.getByText(texts.Body.part1.subHeading2)).toBeDefined();
  });

  it("should render body part 1 text 4", () => {
    expect(screen.getByText(texts.Body.part1.text4)).toBeDefined();
  });

  it("should render body part 2 heading", () => {
    expect(screen.getByText(texts.Body.part2.heading)).toBeDefined();
  });

  it("should render body part 2 intro text", () => {
    expect(screen.getByText(texts.Body.part2.introText)).toBeDefined();
  });

  it("should render body part 2 subheading 2", () => {
    expect(screen.getByText(texts.Body.part2.subHeading2)).toBeDefined();
  });

  it("should render body part 2 text 2", () => {
    expect(screen.getByText(texts.Body.part2.text2)).toBeDefined();
  });

  it("should render body part 3 heading", () => {
    expect(screen.getByText(texts.Body.part3.heading)).toBeDefined();
  });

  it("should render body part 3 subheading 1", () => {
    expect(screen.getByText(texts.Body.part3.subHeading1)).toBeDefined();
  });

  it("should render body part 3 text 2", () => {
    expect(screen.getByText(texts.Body.part3.text2)).toBeDefined();
  });
});

describe("Render boxes", () => {
  beforeEach(() => {
    render(<FreeTaxDeclarationForPensionersPage {...MOCK_PROPS} />);
  });

  it("should render the ContentPageBox component", () => {
    expect(screen.getByText("Content Page Box")).toBeInTheDocument();
  });

  it("should render the SuccessStepsInfoBox component", () => {
    expect(screen.getByText("Steps Info Box")).toBeInTheDocument();
  });
});
