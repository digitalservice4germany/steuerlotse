import React from "react";
import { render, screen } from "@testing-library/react";
import i18n from "i18next";
import { I18nextProvider } from "react-i18next";
import MandateForTaxDeclarationPage from "./MandateForTaxDeclarationPage";

jest.mock("../components/InfoBox", () => ({
  __esModule: true,
  default: function InfoBox() {
    return <div>InfoBox</div>;
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

describe("MandateForTaxDeclaration translations", () => {
  const texts =
    i18n.getDataByLanguage("de").translation.mandateForTaxDeclaration;
  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <MandateForTaxDeclarationPage {...MOCK_PROPS} />
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

  it("should render anchor 4", () => {
    expect(screen.getByText(texts.AnchorList.anchor4)).toBeDefined();
  });

  it("should render accordion heading", () => {
    expect(screen.getByText(texts.Accordion.heading)).toBeDefined();
  });

  it("should render accordion item 1 heading", () => {
    expect(screen.getAllByText(texts.Accordion.Item1.heading)).toBeDefined();
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

  it("should render body part 1 heading", () => {
    expect(screen.getAllByText(texts.Body.part1.heading)).toBeDefined();
  });

  it("should render body part 1 text 2", () => {
    expect(screen.getByText(texts.Body.part1.text2)).toBeDefined();
  });

  it("should render body part 2 heading", () => {
    expect(screen.getByText(texts.Body.part2.heading)).toBeDefined();
  });

  it("should render body part 2 text 2", () => {
    expect(screen.getByText(texts.Body.part2.text1)).toBeDefined();
  });

  it("should render body part 2 list item 1", () => {
    expect(screen.getByText(texts.Body.part2.list.item1)).toBeDefined();
  });

  it("should render body part 2 list item 2", () => {
    expect(screen.getByText(texts.Body.part2.list.item2)).toBeDefined();
  });

  it("should render body part 2 list item 3", () => {
    expect(screen.getByText(texts.Body.part2.list.item3)).toBeDefined();
  });

  it("should render body part 2 list item 4", () => {
    expect(screen.getByText(texts.Body.part2.list.item4)).toBeDefined();
  });

  it("should render body part 2 list item 5", () => {
    expect(screen.getByText(texts.Body.part2.list.item5)).toBeDefined();
  });

  it("should render body part 3 heading", () => {
    expect(screen.getByText(texts.Body.part3.heading)).toBeDefined();
  });

  it("should render body part 3 text 1", () => {
    expect(screen.getByText(texts.Body.part3.text1)).toBeDefined();
  });

  it("should render body part 3 text 2", () => {
    expect(screen.getByText(texts.Body.part3.text2)).toBeDefined();
  });

  it("should render body part 3 subheading 1", () => {
    expect(screen.getByText(texts.Body.part3.subHeading1)).toBeDefined();
  });

  it("should render body part 4 heading", () => {
    expect(screen.getByText(texts.Body.part4.heading)).toBeDefined();
  });

  it("should render body part 4 text 1", () => {
    expect(screen.getByText(texts.Body.part4.text1)).toBeDefined();
  });

  it("should render body part 4 text 2", () => {
    expect(screen.getByText(texts.Body.part4.text2)).toBeDefined();
  });

  it("should render body part 5 heading", () => {
    expect(screen.getByText(texts.Body.part5.heading)).toBeDefined();
  });

  it("should render body part 5 text 1", () => {
    expect(screen.getByText(texts.Body.part5.text1)).toBeDefined();
  });

  it("should render body part 5 text 2", () => {
    expect(screen.getByText(texts.Body.part5.text2)).toBeDefined();
  });
});

describe("Render boxes", () => {
  beforeEach(() => {
    render(<MandateForTaxDeclarationPage {...MOCK_PROPS} />);
  });

  it("should render the InfoBox component", () => {
    expect(screen.getByText("InfoBox")).toBeInTheDocument();
  });

  it("should render the SuccessStepsInfoBox component", () => {
    expect(screen.getByText("Steps Info Box")).toBeInTheDocument();
  });
});
