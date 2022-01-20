import React from "react";
import { render, screen } from "@testing-library/react";
import SessionNotePage from "./SessionNotePage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

const EXPECTED_HEADER = {
  title: "Hinweis zur Sitzung",
};

const DEFAULT_PROPS = {
  form: {
    ...StepFormDefault.args,
  },
  prevUrl: "/some/prev/path",
};

const OVERVIEW_PROPS = {
  form: {
    action: "#form-submit",
    csrfToken: "abc123imacsrftoken",
    showOverviewButton: true,
  },
  prevUrl: "/some/prev/path",
};

describe("SessionNotePage", () => {
  it("should render step title text", () => {
    render(<SessionNotePage {...DEFAULT_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<SessionNotePage {...DEFAULT_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });

  it("should render a next button", () => {
    render(<SessionNotePage {...DEFAULT_PROPS} />);
    expect(screen.getByText("Weiter")).toBeInTheDocument();
    expect(screen.getByText("Weiter").tagName).toEqual("BUTTON");
  });

  it("should not render a button to go to the overview", () => {
    render(<SessionNotePage {...DEFAULT_PROPS} />);
    expect(screen.queryByText("Zurück zur Übersicht")).not.toBeInTheDocument();
  });

  it("should render a button to go to the overview", () => {
    render(<SessionNotePage {...OVERVIEW_PROPS} />);
    expect(screen.getByText("Zurück zur Übersicht")).toBeInTheDocument();
    expect(screen.getByText("Zurück zur Übersicht").tagName).toEqual("BUTTON");
  });
});
