import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldYesNo from "./FormFieldYesNo";

describe("FormFieldYesNo", () => {
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
    render(<FormFieldYesNo {...props} />);
  });

  describe("When Ja clicked", () => {
    beforeEach(() => {
      userEvent.click(screen.getByText("Ja"));
    });

    it("Should activate Ja field", () => {
      expect(screen.getByText("Ja")).toHaveClass("active");
    });

    it("Should check Ja Field", () => {
      expect(screen.getByLabelText("Ja")).toBeChecked();
    });

    it("Should not activate Nein field", () => {
      expect(screen.getByText("Nein")).not.toHaveClass("active");
    });

    it("Should call the change handler with yes", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("yes");
    });
  });

  describe("When Nein clicked", () => {
    beforeEach(() => {
      userEvent.click(screen.getByText("Nein"));
    });

    it("Should activate Nein field", () => {
      expect(screen.getByText("Nein")).toHaveClass("active");
    });

    it("Should check Nein Field", () => {
      expect(screen.getByLabelText("Nein")).toBeChecked();
    });

    it("Should not activate Ja field", () => {
      expect(screen.getByText("Ja")).not.toHaveClass("active");
    });

    it("Should call the change handler with no", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("no");
    });
  });

  describe("When using keyboard input", () => {
    it("Should set focus on yes field when pressing tab", () => {
      userEvent.tab();
      expect(screen.getByLabelText("Ja")).toHaveFocus();
    });

    it("Should keep focus on yes field Focus when pressing tab and then space", () => {
      userEvent.tab();
      userEvent.keyboard(" ");
      expect(screen.getByLabelText("Ja")).toHaveFocus();
    });

    it("Should activate Ja Field when pressing tab and then space", () => {
      userEvent.tab();
      userEvent.keyboard(" ");
      expect(screen.getByText("Ja")).toHaveClass("active");
    });

    it("Should check Ja Field when pressing tab and then space", () => {
      userEvent.tab();
      userEvent.keyboard(" ");
      expect(screen.getByLabelText("Ja")).toBeChecked();
    });

    it("Should focus Nein Field when pressing tab and then right arrow key", () => {
      userEvent.tab();
      // This is currently the only way to trigger an arrow event. userEvent.keyboard('{ArrowRight}'); is not supported yet.
      userEvent.type(screen.getByLabelText("Nein"), "{arrowright}");
      expect(screen.getByLabelText("Nein")).toHaveFocus();
    });

    it("Should activate Nein Field when focussing on Nein field and pressing space", () => {
      userEvent.tab();
      // This is currently the only way to trigger an arrow event. userEvent.keyboard('{ArrowRight}'); is not supported yet.
      userEvent.type(screen.getByLabelText("Nein"), "{arrowright}");
      expect(screen.getByText("Nein")).toHaveClass("active");
    });

    it("Should check Nein Field when focussing on  Nein field and pressing space", () => {
      userEvent.tab();
      // This is currently the only way to trigger an arrow event. userEvent.keyboard('{ArrowRight}'); is not supported yet.
      userEvent.type(screen.getByLabelText("Nein"), "{arrowright}");
      expect(screen.getByLabelText("Nein")).toBeChecked();
    });
  });
});
