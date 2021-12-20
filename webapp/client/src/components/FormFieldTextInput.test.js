import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldTextInput from "./FormFieldTextInput";

describe("FormFieldTextInput", () => {
  let props;

  describe("When default props used", () => {
    beforeEach(() => {
      props = {
        fieldId: "text-input",
        fieldName: "text-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
      };
      render(<FormFieldTextInput {...props} />);
    });

    it("Should set focus on field on tab", () => {
      userEvent.tab();
      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("Should enter keyboard input into input after pressing tab", () => {
      userEvent.tab();
      userEvent.keyboard("Helloo");
      expect(screen.getByLabelText("Label")).toHaveValue("Helloo");
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
        fieldId: "text-input",
        fieldName: "text-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
        fieldWidth: 5,
      };
      render(<FormFieldTextInput {...props} />);
    });

    it("Should not limit input of values", () => {
      userEvent.type(
        screen.getByLabelText("Label"),
        "Supercalifragilisticexpialidocious"
      );
      expect(screen.getByLabelText("Label")).toHaveValue(
        "Supercalifragilisticexpialidocious"
      );
    });

    it("should set width class", () => {
      expect(screen.getByLabelText("Label")).toHaveClass("input-width-5");
    });
  });

  describe("When maxLength given", () => {
    beforeEach(() => {
      props = {
        fieldId: "text-input",
        fieldName: "text-input",
        label: {
          text: "Label",
        },
        errors: [],
        value: "",
        maxLength: 5,
      };
      render(<FormFieldTextInput {...props} />);
    });

    it("Should limit input of values", () => {
      userEvent.type(
        screen.getByLabelText("Label"),
        "Supercalifragilisticexpialidocious"
      );
      expect(screen.getByLabelText("Label")).toHaveValue("Super");
    });

    it("should not set width class", () => {
      expect(screen.getByLabelText("Label")).not.toHaveClass("input-width-5");
    });

    it("Should enter keyboard input into input after pressing tab", () => {
      userEvent.tab();
      userEvent.keyboard("Helloo");
      expect(screen.getByLabelText("Label")).toHaveValue("Hello");
    });
  });
});
