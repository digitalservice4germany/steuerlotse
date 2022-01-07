import React from "react";
import { render, screen } from "@testing-library/react";
import FahrkostenpauschalePage from "./FahrkostenpauschalePage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

const props = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    requestsFahrkostenpauschale: {
      errors: [],
      name: "requests_fahrkostenpauschale",
    },
  },
  fahrkostenpauschaleAmount: "900",
  prevUrl: "/some/prev/path",
};

describe("FahrkostenpauschalePage default", () => {
  beforeEach(() => {
    render(<FahrkostenpauschalePage {...props} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText("Title")).toBeInTheDocument();
  });

  it("should ignore step intro text", () => {
    expect(screen.queryByText("Intro")).not.toBeInTheDocument();
  });

  it("should ignore field option texts", () => {
    expect(screen.queryByLabelText("Ja")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Nein")).not.toBeInTheDocument();
  });

  it("should render yes no fields", () => {
    expect(screen.getByDisplayValue("yes")).toBeInTheDocument();
    expect(screen.getByDisplayValue("no")).toBeInTheDocument();
  });

  it("should render fahrkosten choice fields", () => {
    expect(screen.getByText("Pauschale beantragen")).toBeInTheDocument();
    expect(screen.getByText("Pauschale nicht beantragen")).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });
});

describe("With yes preselected", () => {
  beforeEach(() => {
    let yesProps = {
      ...props,
      fields: {
        requestsFahrkostenpauschale: {
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
          name: "requests_fahrkostenpauschale",
        },
      },
    };
    render(<FahrkostenpauschalePage {...yesProps} />);
  });
  it("should render selected value yes", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(true);
    expect(screen.getByDisplayValue("no").checked).toBe(false);
  });
});

describe("With no preselected", () => {
  beforeEach(() => {
    let noProps = {
      ...props,
      fields: {
        requestsFahrkostenpauschale: {
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
          name: "requests_fahrkostenpauschale",
        },
      },
    };
    render(<FahrkostenpauschalePage {...noProps} />);
  });
  it("should render selected value no", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(false);
    expect(screen.getByDisplayValue("no").checked).toBe(true);
  });
});
