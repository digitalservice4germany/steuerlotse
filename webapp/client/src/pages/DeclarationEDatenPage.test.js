import React from "react";
import { render, screen } from "@testing-library/react";
import { configure } from "@testing-library/dom";
import userEvent from "@testing-library/user-event";
import DeclarationEDatenPage from "./DeclarationEDatenPage";
import avoidSubmitForm from "../lib/submitFormTestHelper";

configure({ testIdAttribute: "id" });

const defaultProps = {
  stepHeader: {
    title: "Title",
  },
  form: {
    action: "#form-submit",
    csrfToken: "abc123imacsrftoken",
  },
  fields: {
    declarationEdaten: {
      checked: false,
      errors: [],
    },
  },
  prevUrl: "/some/prev/path",
};

function setup(optionalProps) {
  const utils = render(
    <DeclarationEDatenPage {...defaultProps} {...optionalProps} />
  );
  const user = userEvent.setup();

  return { ...utils, user };
}

describe("DeclarationEDatenPage", () => {
  avoidSubmitForm();

  it("should render step title text", () => {
    setup();

    expect(screen.getByText("Title")).toBeInTheDocument();
  });

  it("should render back button", () => {
    setup();

    expect(screen.getByText("Zurück")).toBeInTheDocument();
  });

  it("should render checked value false", () => {
    setup();

    expect(screen.getByTestId("declaration_edaten").checked).toBe(false);
  });

  it("should render checked value true", () => {
    setup({
      fields: {
        declarationEdaten: {
          checked: true,
          errors: [],
        },
      },
    });

    expect(screen.getByTestId("declaration_edaten").checked).toBe(true);
  });

  it("should render error value", () => {
    setup({
      fields: {
        declarationEdaten: {
          checked: false,
          errors: ["Error1"],
        },
      },
    });

    expect(screen.getByText("Error1")).toBeInTheDocument();
  });

  it("should call plausible on showOverviewButton click with default goal", async () => {
    const { user } = setup({
      form: {
        action: "#form-submit",
        csrfToken: "abc123imacsrftoken",
        showOverviewButton: true,
      },
      plausibleDomain: "domain/some/link/path",
    });
    const EXPECTED_PLAUSIBLE_GOAL = "Zurück zur Übersicht";
    const EXPECTED_PLAUSIBLE_PROPS = {
      props: { method: "CTA Übernahme vorliegender Daten" },
    };

    window.plausible = jest.fn();

    await user.click(screen.getByText(/Zurück zur Übersicht/));

    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });

  it("should not call plausible if no plausible domain given", async () => {
    const { user } = setup({
      form: {
        action: "#form-submit",
        csrfToken: "abc123imacsrftoken",
        showOverviewButton: true,
      },
    });

    window.plausible = jest.fn();

    await user.click(screen.getByText(/Zurück zur Übersicht/));

    expect(window.plausible).not.toHaveBeenCalled();
  });
});
