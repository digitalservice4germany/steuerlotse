import React from "react";
import { render, screen } from "@testing-library/react";
import FahrtkostenpauschalePage from "./FahrtkostenpauschalePage";
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
    requestsFahrtkostenpauschale: {
      errors: [],
      name: "requests_fahrtkostenpauschale",
    },
  },
  fahrtkostenpauschaleAmount: "900",
  prevUrl: "/some/prev/path",
};

describe("FahrtkostenpauschalePage default", () => {
  beforeEach(() => {
    render(<FahrtkostenpauschalePage {...props} />);
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

  it("should render fahrtkosten choice fields", () => {
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
    const yesProps = {
      ...props,
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
    };
    render(<FahrtkostenpauschalePage {...yesProps} />);
  });
  it("should render selected value yes", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(true);
    expect(screen.getByDisplayValue("no").checked).toBe(false);
  });
});

describe("With no preselected", () => {
  beforeEach(() => {
    const noProps = {
      ...props,
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
    };
    render(<FahrtkostenpauschalePage {...noProps} />);
  });
  it("should render selected value no", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(false);
    expect(screen.getByDisplayValue("no").checked).toBe(true);
  });
});
