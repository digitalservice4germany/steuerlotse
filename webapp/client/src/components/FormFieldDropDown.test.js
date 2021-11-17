import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldDropDown from "./FormFieldDropDown";

describe("FormFieldDropDown", () => {
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
      options: [
        { value: "A", displayName: "Vulcan" },
        { value: "B", displayName: "Terra" },
        { value: "C", displayName: "Earth" },
      ],
      onChangeHandler: onChangeHandler,
    };
    render(<FormFieldDropDown {...props} />);
  });

  describe("When second option has been selected", () => {
    beforeEach(() => {
      userEvent.selectOptions(screen.getByRole("combobox"), ["B"]);
    });

    it("Only second option should be selected", () => {
      expect(screen.getByRole("option", { name: "Vulcan" }).selected).toBe(
        false
      );
      expect(screen.getByRole("option", { name: "Terra" }).selected).toBe(true);
      expect(screen.getByRole("option", { name: "Earth" }).selected).toBe(
        false
      );
    });

    it("Should call the change handler with B", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("B");
    });

    describe("When third option has been selected", () => {
      beforeEach(() => {
        userEvent.selectOptions(screen.getByRole("combobox"), ["C"]);
      });

      it("Only third option should be selected", () => {
        expect(screen.getByRole("option", { name: "Vulcan" }).selected).toBe(
          false
        );
        expect(screen.getByRole("option", { name: "Terra" }).selected).toBe(
          false
        );
        expect(screen.getByRole("option", { name: "Earth" }).selected).toBe(
          true
        );
      });

      it("Should call the change handler with C", () => {
        expect(onChangeHandler).toHaveBeenCalled();

        const changeEvent = onChangeHandler.mock.calls[0][0];
        expect(changeEvent.target.value).toEqual("C");
      });
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("Should set focus on dropDown", () => {
      expect(screen.getByRole("combobox")).toHaveFocus();
    });

    describe("When pressing tab again", () => {
      beforeEach(() => {
        userEvent.tab();
      });

      it("Should not set focus on dropDown", () => {
        expect(screen.getByRole("combobox")).not.toHaveFocus();
      });
    });
  });
});
