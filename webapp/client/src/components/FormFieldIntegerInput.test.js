import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldIntegerInput from "./FormFieldIntegerInput";

describe("FormFieldIntegerInput", () => {
  let props;

  describe("When default props used", () => {
    beforeEach(() => {
      props = {
        fieldId: "integer-input",
        fieldName: "integer-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
      };
      render(<FormFieldIntegerInput {...props} />);
    });

    it("Should not allow input of text", () => {
      userEvent.type(screen.getByRole("textbox"), "Hello World");
      expect(screen.getByLabelText("Label")).toHaveValue("");
    });

    it("Should not allow input of comma", () => {
      userEvent.type(screen.getByRole("textbox"), "123,45");
      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });

    it("Should set focus on field on tab", () => {
      userEvent.tab();
      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("Should enter keyboard input into input after pressing tab", () => {
      userEvent.tab();
      userEvent.keyboard("12345");
      expect(screen.getByLabelText("Label")).toHaveValue("12345");
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
        fieldId: "integer-input",
        fieldName: "integer-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
        fieldWidth: 5,
      };
      render(<FormFieldIntegerInput {...props} />);
    });

    it("Should not limit input of values", () => {
      userEvent.type(screen.getByLabelText("Label"), "12345678910");
      expect(screen.getByLabelText("Label")).toHaveValue("12345678910");
    });

    it("should set width class", () => {
      expect(screen.getByLabelText("Label")).toHaveClass("input-width-5");
    });
  });

  describe("When maxLength given", () => {
    beforeEach(() => {
      props = {
        fieldId: "integer-input",
        fieldName: "integer-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
        maxLength: 5,
      };
      render(<FormFieldIntegerInput {...props} />);
    });

    it("Should limit input of values", () => {
      userEvent.type(screen.getByLabelText("Label"), "12345678910");
      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });

    it("should not set width class", () => {
      expect(screen.getByLabelText("Label")).not.toHaveClass("input-width-5");
    });

    it("Should limit input of values when using keyboard", () => {
      userEvent.tab();
      userEvent.keyboard("123456");
      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });
  });
});
