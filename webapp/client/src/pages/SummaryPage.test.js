import React from "react";
import { configure } from "@testing-library/dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SummaryPage from "./SummaryPage";

configure({ testIdAttribute: "id" });

const MOCK_PROPS = {
  summaryData: {
    section_steps: {
      mandatory_data: {
        data: {
          decl_incomes: {
            data: {
              "Keine weiteren Einkünfte vorhanden:": "Ja",
            },
            label: "Angabe zu weiteren Einkünften",
            url: "/lotse/step/decl_incomes?link_overview=True",
          },
        },
      },
      section_steuerminderung: {
        data: {
          select_stmind: {
            data: {
              "Vorsorgeaufwendungen ausgewählt:": "Ja",
              "Krankheitskosten und weitere außergewöhnliche Belastungen ausgewählt:":
                "Ja",
              "Haushaltsnahe Dienstleistungen und Handwerkerleistungen ausgewählt:":
                "Ja",
              "Spenden und Mitgliedsbeiträge ausgewählt:": "Ja",
              "Steuern für Ihre Religionsgemeinschaft ausgwählt:": "Ja",
            },
            label: "Ihre Ausgaben",
            url: "/lotse/step/select_stmind?link_overview=True",
          },
        },
      },
    },
  },
};

const REQUIRED_PROPS = {
  form: {
    action: "#form-submit",
    csrfToken: "abc123imacsrftoken",
  },
  prevUrl: "/some/prev/path",
  fields: {
    declarationSummary: {
      checked: false,
      errors: [],
    },
  },
};

function setup(optionalProps) {
  const utils = render(
    <SummaryPage {...MOCK_PROPS} {...REQUIRED_PROPS} {...optionalProps} />
  );
  const backButton = screen.getByText("Zurück");
  const nextButton = screen.getByText("Weiter");
  const user = userEvent.setup();

  return { ...utils, backButton, user, nextButton };
}

describe("SummaryPage", () => {
  it("Should render the Header text", () => {
    setup();
    const EXPECTED_HEADER = {
      title: "Prüfen Sie Ihre Angaben",
      mandatoryHeading: "PFLICHTANGABEN",
      sectionSteuerminderungHeading: "STEUERMINDERNDE AUFWENDUNGEN",
    };

    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
    expect(
      screen.getByText(EXPECTED_HEADER.mandatoryHeading)
    ).toBeInTheDocument();
    expect(
      screen.getByText(EXPECTED_HEADER.sectionSteuerminderungHeading)
    ).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    const { backButton } = setup();

    expect(backButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.prevUrl)
    );
  });

  it("should render checked value false", () => {
    setup();

    expect(screen.getByTestId("declaration_summary").checked).toBe(false);
  });

  it("should render checked value true", () => {
    setup({
      fields: {
        declarationSummary: {
          checked: true,
          errors: [],
        },
      },
    });

    expect(screen.getByTestId("declaration_summary").checked).toBe(true);
  });

  it("should render error value", () => {
    setup({
      fields: {
        declarationSummary: {
          checked: false,
          errors: ["Error1"],
        },
      },
    });

    expect(screen.getByText("Error1")).toBeInTheDocument();
  });
});
