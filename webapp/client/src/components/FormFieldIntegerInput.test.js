import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldIntegerInput from "./FormFieldIntegerInput";

describe("FormFieldIntegerInput", () => {
  let props;

  describe("When default props used", () => {
    const user = userEvent.setup();

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

    it("should not allow input of text", async () => {
      await user.type(screen.getByRole("textbox"), "Hello World");

      expect(screen.getByLabelText("Label")).toHaveValue("");
    });

    it("should not allow input of comma", async () => {
      await user.type(screen.getByRole("textbox"), "123,45");

      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });

    it("should set focus on textbox field when pressing tab", async () => {
      await user.tab();

      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("should enter keyboard input into input after pressing tab", async () => {
      await user.tab();
      await user.keyboard("12345");

      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });

    it("should remove focus from field when pressing tab two times", async () => {
      await user.tab();
      await user.tab();

      expect(screen.getByRole("textbox")).not.toHaveFocus();
    });
  });

  describe("When fieldWidth given", () => {
    const user = userEvent.setup();

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

    it("should not limit input of values", async () => {
      await user.type(screen.getByLabelText("Label"), "12345678910");

      expect(screen.getByLabelText("Label")).toHaveValue("12345678910");
    });

    it("should set width class", () => {
      expect(screen.getByLabelText("Label")).toHaveClass("input-width-5");
    });
  });

  describe("When maxLength given", () => {
    const user = userEvent.setup();

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

    it("should limit input of values", async () => {
      await user.type(screen.getByLabelText("Label"), "12345678910");

      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });

    it("should not set width class", () => {
      expect(screen.getByLabelText("Label")).not.toHaveClass("input-width-5");
    });

    it("should limit input of values when using keyboard", async () => {
      await user.tab();
      await user.keyboard("123456");

      expect(screen.getByLabelText("Label")).toHaveValue("12345");
    });
  });
});
