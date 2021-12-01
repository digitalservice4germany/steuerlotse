import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldTextInput from "./FormFieldTextInput";

describe("FormFieldTextInput", () => {
  let props;

  describe("Base Field", () => {
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

    describe("When pressing tab", () => {
      beforeEach(() => {
        userEvent.tab();
      });

      it("Should set focus on field", () => {
        expect(screen.getByRole("textbox")).toHaveFocus();
      });

      describe("When pressing tab again", () => {
        beforeEach(() => {
          userEvent.tab();
        });

        it("Should unset focus on field", () => {
          expect(screen.getByRole("textbox")).not.toHaveFocus();
        });
      });
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

    it("Should not limit input of values", () => {
      userEvent.type(
        screen.getByLabelText("Label"),
        "Supercalifragilisticexpialidocious"
      );
      expect(screen.getByLabelText("Label")).toHaveValue(
        "Supercalifragilisticexpialidocious"
      );
    });
  });

  describe("When maxLength given and setMaxLength true", () => {
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
        setMaxLength: true,
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
  });
});
