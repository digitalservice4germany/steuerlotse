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

    it("Activate Ja field", () => {
      expect(screen.getByText("Ja")).toHaveClass("active");
    });

    it("Check Ja Field", () => {
      expect(screen.getByLabelText("Ja")).toBeChecked();
    });

    it("Do not activate Nein field", () => {
      expect(screen.getByText("Nein")).not.toHaveClass("active");
    });

    it("Call the change handler with yes", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("yes");
    });
  });

  describe("When Nein clicked", () => {
    beforeEach(() => {
      userEvent.click(screen.getByText("Nein"));
    });

    it("Activate Nein field", () => {
      expect(screen.getByText("Nein")).toHaveClass("active");
    });

    it("Check Nein Field", () => {
      expect(screen.getByLabelText("Nein")).toBeChecked();
    });

    it("Do not activate Ja field", () => {
      expect(screen.getByText("Ja")).not.toHaveClass("active");
    });

    it("Call the change handler with no", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("no");
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("set focus on yes field", () => {
      expect(screen.getByLabelText("Ja")).toHaveFocus();
    });

    describe("When pressing space", () => {
      beforeEach(() => {
        userEvent.keyboard(" ");
      });

      it("Focus Ja Field", () => {
        expect(screen.getByLabelText("Ja")).toHaveFocus();
      });

      it("Activate Ja Field", () => {
        expect(screen.getByText("Ja")).toHaveClass("active");
      });

      it("Check Ja Field", () => {
        expect(screen.getByLabelText("Ja")).toBeChecked();
      });
    });

    describe("When pressing right arrow key", () => {
      beforeEach(() => {
        userEvent.type(screen.getByLabelText("Nein"), "{arrowright}");
      });

      it("Focus Nein Field", () => {
        expect(screen.getByLabelText("Nein")).toHaveFocus();
      });

      it("Activate Nein Field", () => {
        expect(screen.getByText("Nein")).toHaveClass("active");
      });

      it("Check Nein Field", () => {
        expect(screen.getByLabelText("Nein")).toBeChecked();
      });
    });
  });
});
