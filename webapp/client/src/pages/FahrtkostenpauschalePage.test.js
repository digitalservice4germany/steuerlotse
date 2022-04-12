import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FahrtkostenpauschalePage from "./FahrtkostenpauschalePage";
import avoidNotImplementedFormSubmitError from "../test-helper/submitFormTestHelper";

const defaultProps = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  form: {
    action: "#form-submit",
    csrfToken: "abc123imacsrftoken",
  },
  fields: {
    requestsFahrtkostenpauschale: {
      errors: [],
      name: "requests_fahrtkostenpauschale",
    },
  },
  fahrtkostenpauschaleAmount: "900",
  prevUrl: "/some/prev/path",
};

function setup(optionalProps) {
  const utils = render(
    <FahrtkostenpauschalePage {...defaultProps} {...optionalProps} />
  );
  const user = userEvent.setup();

  return { ...utils, user };
}

describe("FahrtkostenpauschalePage default", () => {
  avoidNotImplementedFormSubmitError();

  it("should render step title text", () => {
    setup();

    expect(screen.getByText("Title")).toBeInTheDocument();
  });

  it("should ignore step intro text", () => {
    setup();

    expect(screen.queryByText("Intro")).not.toBeInTheDocument();
  });

  it("should ignore field option texts", () => {
    setup();

    expect(screen.queryByLabelText("Ja")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Nein")).not.toBeInTheDocument();
  });

  it("should render yes no fields", () => {
    setup();

    expect(screen.getByDisplayValue("yes")).toBeInTheDocument();
    expect(screen.getByDisplayValue("no")).toBeInTheDocument();
  });

  it("should render fahrtkosten choice fields", () => {
    setup();

    expect(screen.getByText("Pauschale beantragen")).toBeInTheDocument();
    expect(screen.getByText("Pauschale nicht beantragen")).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    setup();

    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });
});

it("should render with preselected value yes checked", () => {
  setup({
    fields: {
      requestsFahrtkostenpauschale: {
        selectedValue: "yes",
        options: [
          {
            value: "yes",
            displayName: "Ja",
          },
          {
            value: "no",
            displayName: "Nein",
          },
        ],
        errors: [],
        name: "requests_fahrtkostenpauschale",
      },
    },
  });

  expect(screen.getByDisplayValue("yes").checked).toBe(true);
  expect(screen.getByDisplayValue("no").checked).toBe(false);
});

it("should render with pre selected value no checked", () => {
  setup({
    fields: {
      requestsFahrtkostenpauschale: {
        selectedValue: "no",
        options: [
          {
            value: "yes",
            displayName: "Ja",
          },
          {
            value: "no",
            displayName: "Nein",
          },
        ],
        errors: [],
        name: "requests_fahrtkostenpauschale",
      },
    },
  });

  expect(screen.getByDisplayValue("yes").checked).toBe(false);
  expect(screen.getByDisplayValue("no").checked).toBe(true);
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
    props: undefined,
  };

  window.plausible = jest.fn();

  await user.click(screen.getByText(/Zurück zur Übersicht/));

  expect(window.plausible).toHaveBeenCalledWith(
    EXPECTED_PLAUSIBLE_GOAL,
    EXPECTED_PLAUSIBLE_PROPS
  );
});
