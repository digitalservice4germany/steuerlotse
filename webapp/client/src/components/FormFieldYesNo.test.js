import React from "react";
import { render, screen } from "@testing-library/react";
import { fireEvent } from "@testing-library/dom";
import FormFieldYesNo from "./FormFieldYesNo";

describe("FormFieldYesNo", () => {
  let props;

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
      },
      errors: [],
    };
  });

  it("should activate the Yes field when Ja has been clicked", () => {
    render(<FormFieldYesNo {...props} />);
    fireEvent.click(screen.getByText("Ja"));
    expect(screen.getByText("Ja")).toHaveClass("active");
    expect(screen.getByText("Nein")).not.toHaveClass("active");
  });

  it("should activate the No field when Nein has been clicked", () => {
    render(<FormFieldYesNo {...props} />);
    fireEvent.click(screen.getByText("Nein"));
    expect(screen.getByText("Nein")).toHaveClass("active");
    expect(screen.getByText("Ja")).not.toHaveClass("active");
  });
});

describe("FormFieldYesNo with an onChangeHandler", () => {
  let props;

  const onChangeHandler = jest.fn();

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
      },
      errors: [],
      onChangeHandler: onChangeHandler,
    };
  });

  it("should call the change handler when Ja has been clicked", () => {
    render(<FormFieldYesNo {...props} />);
    fireEvent.click(screen.getByText("Ja"));
    expect(onChangeHandler).toHaveBeenCalled();
  });

  it("should call the change handler when Nein has been clicked", () => {
    render(<FormFieldYesNo {...props} />);
    fireEvent.click(screen.getByText("Nein"));
    expect(onChangeHandler).toHaveBeenCalled();
  });
});
