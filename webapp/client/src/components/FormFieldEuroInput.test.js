import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldEuroInput from "./FormFieldEuroInput";

const MOCK_PROPS = {
  fieldId: "euro-input",
  fieldName: "euro-input",
  label: {
    text: "Label",
  },
  errors: [],
  value: "",
};

describe("FormFieldEuroInput", () => {
  const user = userEvent.setup();

  describe("When default props used", () => {
    beforeEach(() => {
      render(<FormFieldEuroInput {...MOCK_PROPS} />);
    });

    it("should not allow input of text", async () => {
      await user.type(screen.getByRole("textbox"), "Hello World");

      expect(screen.getByLabelText("Label")).toHaveValue("");
    });

    it("should allow input of comma", async () => {
      await user.type(screen.getByRole("textbox"), "123,45");

      expect(screen.getByLabelText("Label")).toHaveValue("123,45");
    });

    it("should allow input of point as thousands separator", async () => {
      await user.type(screen.getByRole("textbox"), "1.023,45");

      expect(screen.getByLabelText("Label")).toHaveValue("1.023,45");
    });

    it("should not allow more than 2 decimal places", async () => {
      await user.type(screen.getByRole("textbox"), "123,435");

      expect(screen.getByLabelText("Label")).toHaveValue("123,43");
    });

    it("should set focus on field on tab", async () => {
      await user.tab();

      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("should enter keyboard input into input after pressing tab", async () => {
      await user.tab();
      await user.keyboard("123,45");

      expect(screen.getByLabelText("Label")).toHaveValue("123,45");
    });

    it("should unset focus on field when pressing tab two times", async () => {
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
    const MOCK_PROPS_FIELD_WIDTH = { ...MOCK_PROPS, fieldWidth: 5 };

    beforeEach(() => {
      render(<FormFieldEuroInput {...MOCK_PROPS_FIELD_WIDTH} />);
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
    const MOCK_PROPS_MAX_LENGTH = { ...MOCK_PROPS, maxLength: 5 };

    beforeEach(() => {
      render(<FormFieldEuroInput {...MOCK_PROPS_MAX_LENGTH} />);
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
