import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldEuroInput from "./FormFieldEuroInput";

describe("FormFieldEuroInput", () => {
  let props;

  describe("When default props used", () => {
    beforeEach(() => {
      props = {
        fieldId: "euro-input",
        fieldName: "euro-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
      };
      render(<FormFieldEuroInput {...props} />);
    });

    it("Should not allow input of text", () => {
      userEvent.type(screen.getByRole("textbox"), "Hello World");
      expect(screen.getByLabelText("Label")).toHaveValue("");
    });

    it("Should allow input of comma", () => {
      userEvent.type(screen.getByRole("textbox"), "123,45");
      expect(screen.getByLabelText("Label")).toHaveValue("123,45");
    });

    it("Should not allow more than 2 decimal places", () => {
      userEvent.type(screen.getByRole("textbox"), "123,435");
      expect(screen.getByLabelText("Label")).toHaveValue("123,43");
    });

    it("Should set focus on field on tab", () => {
      userEvent.tab();
      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("Should enter keyboard input into input after pressing tab", () => {
      userEvent.tab();
      userEvent.keyboard("123,45");
      expect(screen.getByLabelText("Label")).toHaveValue("123,45");
    });

    it("Should unset focus on field when pressing tab two times", () => {
      userEvent.tab();
      userEvent.tab();
      expect(screen.getByRole("textbox")).not.toHaveFocus();
    });
  });

  describe("When fieldWidth given", () => {
    beforeEach(() => {
      props = {
        fieldId: "euro-input",
        fieldName: "euro-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
        fieldWidth: 5,
      };
      render(<FormFieldEuroInput {...props} />);
    });

    it("Should not limit input of values", () => {
      userEvent.type(screen.getByLabelText("Label"), "12345678910");
      expect(screen.getByLabelText("Label")).toHaveValue("12345678910");
    });

    it("should set width class", () => {
      expect(screen.getByText("€").parentNode).toHaveClass("input-width-5");
    });
  });

  describe("When maxLength given", () => {
    beforeEach(() => {
      props = {
        fieldId: "euro-input",
        fieldName: "euro-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
        maxLength: 5,
      };
      render(<FormFieldEuroInput {...props} />);
    });

    it("Should limit input of values", () => {
      userEvent.type(screen.getByLabelText("Label"), "123456789,10");
      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });

    it("should not set width class", () => {
      expect(screen.getByLabelText("Label")).not.toHaveClass("input-width-5");
    });

    it("Should limit input of values when using keyboard", () => {
      userEvent.tab();
      userEvent.keyboard("123,456");
      expect(screen.getByLabelText("Label")).toHaveValue("123,4");
    });
  });
});
