import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldEuroInput from "./FormFieldEuroInput";

describe("FormFieldEuroInput", () => {
  let props;

  describe("When default props used", () => {
    const user = userEvent.setup();

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

    it("should not allow input of text", async () => {
      await user.type(screen.getByRole("textbox"), "Hello World");

      expect(screen.getByLabelText("Label")).toHaveValue("");
    });

    it("should allow comma as input", async () => {
      await user.type(screen.getByRole("textbox"), "123,45");

      expect(screen.getByLabelText("Label")).toHaveValue("123,45");
    });

    it("should allow point as thousands separator input", async () => {
      await user.type(screen.getByRole("textbox"), "1.023,45");

      expect(screen.getByLabelText("Label")).toHaveValue("1.023,45");
    });

    it("should not allow more than 2 decimal places", async () => {
      await user.type(screen.getByRole("textbox"), "123,435");

      expect(screen.getByLabelText("Label")).toHaveValue("123,43");
    });

    it("should set focus on textbox field when pressing tab", async () => {
      await user.tab();

      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("should enter keyboard input into input after pressing tab", async () => {
      await user.tab();
      await user.keyboard("123,45");

      expect(screen.getByLabelText("Label")).toHaveValue("123,45");
    });

    it("should remove focus from textbox field when pressing tab two times", async () => {
      await user.tab();
      await user.tab();

      expect(screen.getByRole("textbox")).not.toHaveFocus();
    });

    it("should pad fractional zeroes when focus is lost", async () => {
      await user.tab();
      await user.keyboard("123");
      await user.tab();

      expect(screen.getByLabelText("Label")).toHaveValue("123,00");
    });
  });

  describe("When fieldWidth given", () => {
    const user = userEvent.setup();

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

    it("should not limit input of values", async () => {
      await user.type(screen.getByLabelText("Label"), "12345678910");

      expect(screen.getByLabelText("Label")).toHaveValue("12.345.678.910");
    });

    it("should set width class", () => {
      expect(screen.getByText("€").parentNode).toHaveClass("input-width-5");
    });
  });

  describe("When maxLength given", () => {
    const user = userEvent.setup();

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

    it("should limit pre-decimals but not decimals", async () => {
      await user.type(screen.getByLabelText("Label"), "12345");

      expect(screen.getByLabelText("Label")).toHaveValue("12.345");

      await user.type(screen.getByLabelText("Label"), ",99");

      expect(screen.getByLabelText("Label")).toHaveValue("12.345,99");
    });

    it("should not set width class", () => {
      expect(screen.getByLabelText("Label")).not.toHaveClass("input-width-5");
    });

    it("should limit input of values when using keyboard", async () => {
      await user.tab();
      await user.keyboard("12345,565");

      expect(screen.getByLabelText("Label")).toHaveValue("12.345,56");
    });
  });
});
