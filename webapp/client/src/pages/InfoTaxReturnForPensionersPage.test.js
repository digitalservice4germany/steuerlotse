import React from "react";
import { render, screen } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import i18n from "i18next";
import InfoTaxReturnForPensionersPage from "./InfoTaxReturnForPensionersPage";

const MOCK_PROPS = {
  plausibleDomain: "/plausibleDomain/path",
  url: "/eligibility/step/marital_status?link_overview=False",
  contactUsUrl: "mailto:kontakt@steuerlotse-rente.de",
  howItWorksLink: "/sofunktionierts",
};

describe("InfoTaxReturnForPensionersPage", () => {
  it("should render the InfoTaxReturnForPensionersPage component", () => {
    render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);
  });

  beforeEach(() => {
    render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);
  });

  // it("should pass with the Plausible Domain", () => {
  //   expect(screen.getByText("Fragebogen starten")).toHaveAttribute(
  //     "plausibleDomain",
  //     expect.stringContaining(MOCK_PROPS.plausibleDomain)
  //   );
  // });

  it("should render Start Questionnaire button with Link", () => {
    expect(screen.getByText("Fragebogen starten")).toBeInTheDocument();
    expect(screen.getByText("Fragebogen starten").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.url)
    );
  });

  it("should render Contact Us button with Link", () => {
    expect(screen.getByText("Kontaktieren Sie uns")).toBeInTheDocument();
    expect(
      screen.getByText("Kontaktieren Sie uns").closest("a")
    ).toHaveAttribute("href", expect.stringContaining(MOCK_PROPS.contactUsUrl));
  });

  it("should render more information tax guide button", () => {
    expect(screen.getByText("Häufig gestellte Fragen")).toBeInTheDocument();
    expect(
      screen.getByText("Häufig gestellte Fragen").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.howItWorksLink)
    );
  });
});

describe("InfoTaxReturnForPensionersPage Translations", () => {
  const infoTaxReturnPensionersTexts =
    i18n.getDataByLanguage("de").translation.infoTaxReturnPensioners;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <InfoTaxReturnForPensionersPage {...MOCK_PROPS} />
      </I18nextProvider>
    );
  });

  it("Should render the Intro Header", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.intro.heading)
    ).toBeDefined();
  });

  it("Should render the Intro Paragraph", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.intro.paragraphOne)
    ).toBeDefined();
  });

  it("Should render the Intro Paragraph Two", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.intro.paragraphOne)
    ).toBeDefined();
  });

  it("Should render the second section heading", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_two.heading)
    ).toBeDefined();
  });

  it("Should render the second section paragraph", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_two.paragraph)
    ).toBeDefined();
  });

  // it("Should render the third section heading", () => {
  //   expect(
  //     screen.getByText(infoTaxReturnPensionersTexts.section_three.heading)
  //   ).toBeDefined();
  // });

  it("Should render the third section first paragraph", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_three.paragraphOne)
    ).toBeDefined();
  });

  it("Should render the third section second paragraph", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_three.paragraphTwo)
    ).toBeDefined();
  });

  it("Should render the fourth section heading", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_four.heading)
    ).toBeDefined();
  });

  it("Should render the fourth section paragraph", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_four.paragraph)
    ).toBeDefined();
  });

  it("Should render the fifth section first list item heading", () => {
    expect(
      screen.getByText(
        infoTaxReturnPensionersTexts.section_five.listItemOneHeading
      )
    ).toBeDefined();
  });

  it("Should render the fifth section first list item", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_five.listItemOne)
    ).toBeDefined();
  });

  it("Should render the fifth section second list item heading", () => {
    expect(
      screen.getByText(
        infoTaxReturnPensionersTexts.section_five.listItemTwoHeading
      )
    ).toBeDefined();
  });

  it("Should render the fifth section second list item", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_five.listItemTwo)
    ).toBeDefined();
  });

  it("Should render the fifth section third list item heading", () => {
    expect(
      screen.getByText(
        infoTaxReturnPensionersTexts.section_five.listItemThreeHeading
      )
    ).toBeDefined();
  });
  it("Should render the fifth section third list item", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_five.listItemThree)
    ).toBeDefined();
  });

  it("Should render the fifth section fourth list item heading", () => {
    expect(
      screen.getByText(
        infoTaxReturnPensionersTexts.section_five.listItemFourHeading
      )
    ).toBeDefined();
  });

  it("Should render the fifth section fourth list item", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_five.listItemFour)
    ).toBeDefined();
  });

  it("Should render the sixth section text", () => {
    expect(
      screen.getByText(infoTaxReturnPensionersTexts.section_six.text)
    ).toBeDefined();
  });
});

describe("TaxGuideQuestionBox Translations", () => {
  const taxGuideQuestionsBoxTexts =
    i18n.getDataByLanguage("de").translation.taxGuideQuestionBox;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <InfoTaxReturnForPensionersPage {...MOCK_PROPS} />
      </I18nextProvider>
    );
  });

  it("Should render the can I use tax guide text", () => {
    expect(
      screen.getByText(taxGuideQuestionsBoxTexts.canIUseTaxGuide)
    ).toBeDefined();
  });

  it("Should render the start questionnaire text", () => {
    expect(
      screen.getByText(taxGuideQuestionsBoxTexts.startQuestionnaire)
    ).toBeDefined();
  });

  it("Should render the more information tax guide text", () => {
    expect(
      screen.getByText(taxGuideQuestionsBoxTexts.moreInformationTaxGuide)
    ).toBeDefined();
  });

  it("Should render the faq text", () => {
    expect(screen.getByText(taxGuideQuestionsBoxTexts.faq)).toBeDefined();
  });

  it("Should render the contact us text", () => {
    expect(screen.getByText(taxGuideQuestionsBoxTexts.contactUs)).toBeDefined();
  });
});

describe("InfoTaxReturnForPensionersPage without plausible", () => {
  beforeEach(() => {
    render(<InfoTaxReturnForPensionersPage />);
  });

  it("should pass without Plausible Domain", () => {
    expect(screen.getByText("Fragebogen starten")).not.toHaveAttribute(
      "plausibleDomain",
      expect.stringContaining(MOCK_PROPS.plausibleDomain)
    );
  });
});

// test the questions box buttons are there - test text is found DONE
// test the button links to a url - test the URL prop is there cannot be attribute DONE
// test the component renders with props - DONE
// test translations - DONE

// test the button has a plausibleName prop
