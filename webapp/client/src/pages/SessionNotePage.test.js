import React from "react";
import { render, screen } from "@testing-library/react";
import SessionNotePage from "./SessionNotePage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

const EXPECTED_HEADER = {
  title: "Hinweis zur Sitzung",
};

describe("with default props", () => {
  beforeEach(() => {
    const defaultProps = {
      form: {
        ...StepFormDefault.args,
      },
      prevUrl: "/some/prev/path",
    };
    render(<SessionNotePage {...defaultProps} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });

  it("should render a next button", () => {
    expect(screen.getByText("Weiter")).toBeInTheDocument();
    expect(screen.getByText("Weiter").tagName).toEqual("BUTTON");
  });

  it("should not render a button to go to the overview", () => {
    expect(screen.queryByText("Zurück zur Übersicht")).not.toBeInTheDocument();
  });
});

describe("with overview props", () => {
  beforeEach(() => {
    const overviewProps = {
      form: {
        action: "#form-submit",
        csrfToken: "abc123imacsrftoken",
        showOverviewButton: true,
      },
      prevUrl: "/some/prev/path",
    };
    render(<SessionNotePage {...overviewProps} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });

  it("should render a next button", () => {
    expect(screen.getByText("Weiter")).toBeInTheDocument();
    expect(screen.getByText("Weiter").tagName).toEqual("BUTTON");
  });

  it("should render a button to go to the overview", () => {
    expect(screen.getByText("Zurück zur Übersicht")).toBeInTheDocument();
    expect(screen.getByText("Zurück zur Übersicht").tagName).toEqual("BUTTON");
  });
});
