import React from "react";
import { render, screen } from "@testing-library/react";
import { fireEvent } from "@testing-library/dom";
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
        ["A", "Vulcan"],
        ["B", "Terra"],
        ["C", "Earth"],
      ],
      onChangeHandler: onChangeHandler,
    };
    render(<FormFieldDropDown {...props} />);
  });

  describe("When second option selected", () => {
    beforeEach(() => {
      userEvent.selectOptions(screen.getByRole("combobox"), ["B"]);
    });

    it("Only second option has been selected", () => {
      expect(screen.getByRole("option", { name: "Vulcan" }).selected).toBe(
        false
      );
      expect(screen.getByRole("option", { name: "Terra" }).selected).toBe(true);
      expect(screen.getByRole("option", { name: "Earth" }).selected).toBe(
        false
      );
    });

    it("Call the change handler with B", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("B");
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("set focus on dropDown", () => {
      expect(screen.getByRole("combobox")).toHaveFocus();
    });

    describe("When pressing space", () => {
      beforeEach(() => {
        userEvent.keyboard(" ");
        userEvent.keyboard("{arrowDown}");
        userEvent.keyboard(" ");
      });

      it("Only first option has been selected", () => {
        expect(screen.getByRole("option", { name: "Vulcan" }).selected).toBe(
          true
        );
        expect(screen.getByRole("option", { name: "Terra" }).selected).toBe(
          false
        );
        expect(screen.getByRole("option", { name: "Earth" }).selected).toBe(
          false
        );
      });
    });
  });
});
