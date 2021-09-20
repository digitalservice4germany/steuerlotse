import React from "react";
import { render, screen } from "@testing-library/react";
import FormFieldSeparatedField from "./FormFieldSeparatedField";

describe("FormFieldSeparatedField", () => {
  let props;

  beforeEach(() => {
    props = {
      fieldName: "foo",
      fieldId: "foo",
      values: ["bar", "baz"],
      inputFieldLengths: [3, 4],
      errors: [],
      labelComponent: <></>,
      subFieldSeparator: "SPLITTO",
    };
  });

  it("should show the values", () => {
    render(<FormFieldSeparatedField {...props} />);
    expect(screen.getByDisplayValue("bar")).toBeInTheDocument();
    expect(screen.getByDisplayValue("baz")).toBeInTheDocument();
  });

  it("should assign the correct ids", () => {
    render(<FormFieldSeparatedField {...props} />);
    expect(screen.getByDisplayValue("bar")).toHaveAttribute("id", "foo_1");
    expect(screen.getByDisplayValue("baz")).toHaveAttribute("id", "foo_2");
  });

  it("should set the lenghts", () => {
    render(<FormFieldSeparatedField {...props} />);
    const bar = screen.getByDisplayValue("bar");
    expect(bar).toHaveAttribute("maxlength", "3");
    expect(bar).toHaveAttribute("data-field-length", "3");
  });

  it("should show field separators", () => {
    render(<FormFieldSeparatedField {...props} />);
    expect(screen.getByText("SPLITTO")).toBeInTheDocument();
  });
});
