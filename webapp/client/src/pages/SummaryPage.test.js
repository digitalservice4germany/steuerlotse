import React from "react";
import { configure } from "@testing-library/dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SummaryPage from "./SummaryPage";

configure({ testIdAttribute: "id" });

const MOCK_PROPS = {
  summaryData: {
    mandatoryData: {
      data: [
        {
          data: [
            {
              name: "Keine weiteren Einkünfte vorhanden:",
              value: "Ja",
            },
          ],
          label: "Angabe zu weiteren Einkünften",
          url: "/lotse/step/decl_incomes?link_overview=True",
        },
      ],
      label: "Pflichtangaben",
      name: "mandatory_data",
      url: "/lotse/step/decl_incomes?link_overview=True",
    },
    sectionSteuerminderung: {
      data: [
        {
          data: [
            {
              name: "Vorsorgeaufwendungen ausgewählt:",
              value: "Ja",
            },
            {
              name: "Krankheitskosten und weitere außergewöhnliche Belastungen ausgewählt:",
              value: "Ja",
            },
            {
              name: "Haushaltsnahe Dienstleistungen und Handwerkerleistungen ausgewählt:",
              value: "Ja",
            },
            {
              name: "Spenden und Mitgliedsbeiträge ausgewählt:",
              value: "Ja",
            },
            {
              name: "Steuern für Ihre Religionsgemeinschaft ausgwählt:",
              value: "Ja",
            },
          ],
          label: "Ihre Ausgaben",
          url: "/lotse/step/select_stmind?link_overview=True",
        },
      ],
      label: "Steuermindernde Aufwendungen",
      name: "section_steuerminderung",
      url: "/lotse/step/select_stmind?link_overview=True",
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
    confirmCompleteCorrect: {
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

    expect(screen.getByTestId("confirm_complete_correct").checked).toBe(false);
  });

  it("should render checked value true", () => {
    setup({
      fields: {
        confirmCompleteCorrect: {
          checked: true,
          errors: [],
        },
      },
    });

    expect(screen.getByTestId("confirm_complete_correct").checked).toBe(true);
  });

  it("should render error value", () => {
    setup({
      fields: {
        confirmCompleteCorrect: {
          checked: false,
          errors: ["Error1"],
        },
      },
    });

    expect(screen.getByText("Error1")).toBeInTheDocument();
  });
});
