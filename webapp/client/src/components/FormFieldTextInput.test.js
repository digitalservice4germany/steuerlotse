import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldTextInput from "./FormFieldTextInput";

describe("FormFieldTextInput", () => {
  let props;

  describe("When default props used", () => {
    const user = userEvent.setup();

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

    it("should set focus on field when pressing tab", async () => {
      await user.tab();

      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    it("should enter keyboard input into input after pressing tab", async () => {
      await user.tab();
      await user.keyboard("Helloo");

      expect(screen.getByLabelText("Label")).toHaveValue("Helloo");
    });

    it("Should remove focus from field when pressing tab two times", async () => {
      await user.tab();
      await user.tab();

      expect(screen.getByRole("textbox")).not.toHaveFocus();
    });
  });

  describe("When fieldWidth given", () => {
    const user = userEvent.setup();

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

    it("should not limit input of values", async () => {
      await user.type(
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
    const user = userEvent.setup();

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

    it("should limit input of values", async () => {
      await user.type(
        screen.getByLabelText("Label"),
        "Supercalifragilisticexpialidocious"
      );

      expect(screen.getByLabelText("Label")).toHaveValue("Super");
    });

    it("should not set width class", () => {
      expect(screen.getByLabelText("Label")).not.toHaveClass("input-width-5");
    });

    it("should enter keyboard input into input after pressing tab", async () => {
      await user.tab();
      await user.keyboard("Helloo");

      expect(screen.getByLabelText("Label")).toHaveValue("Hello");
    });
  });
});
