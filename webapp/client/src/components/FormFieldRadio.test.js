import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldRadio from "./FormFieldRadio";

describe("FormFieldRadio", () => {
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
    render(<FormFieldRadio {...props} />);
  });

  describe("When label is clicked", () => {
    beforeEach(() => {
      userEvent.click(screen.getByText("Vulcan"));
    });

    it("Correct input is selected ", () => {
      expect(screen.getByLabelText("Vulcan").checked).toEqual(true);
    });

    it("Other inputs are not selected ", () => {
      expect(screen.getByLabelText("Terra").checked).toEqual(false);
      expect(screen.getByLabelText("Earth").checked).toEqual(false);
    });
  });

  describe("When second option has been selected", () => {
    beforeEach(() => {
      userEvent.click(screen.getByLabelText("Terra"));
    });

    it("Only second option should be selected", () => {
      expect(screen.getByRole("radio", { name: "Vulcan" }).checked).toBe(false);
      expect(screen.getByRole("radio", { name: "Terra" }).checked).toBe(true);
      expect(screen.getByRole("radio", { name: "Earth" }).checked).toBe(false);
    });

    it("Should call the change handler with B", () => {
      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("B");
    });
  });

  it("When pressing tab it should set focus on first radio button", () => {
    userEvent.tab();
    expect(screen.getByRole("radio", { name: "Vulcan" })).toHaveFocus();
  });

  it("When pressing tab two times it should unfocus all radio buttons", () => {
    userEvent.tab();
    userEvent.tab();
    expect(screen.getByRole("radio", { name: "Vulcan" })).not.toHaveFocus();
    expect(screen.getByRole("radio", { name: "Terra" })).not.toHaveFocus();
    expect(screen.getByRole("radio", { name: "Earth" })).not.toHaveFocus();
  });

  it("When pressing tab and arrow right it should set focus on second radio button", () => {
    userEvent.tab();
    // This is currently the only way to trigger an arrow event. userEvent.keyboard('{ArrowRight}'); is not supported yet.
    userEvent.type(
      screen.getByRole("radio", { name: "Terra" }),
      "{arrowright}"
    );
    expect(screen.getByRole("radio", { name: "Terra" })).toHaveFocus();
  });

  it("When pressing tab and arrow right it should check second radio button", () => {
    userEvent.tab();
    // This is currently the only way to trigger an arrow event. userEvent.keyboard('{ArrowRight}'); is not supported yet.
    userEvent.type(
      screen.getByRole("radio", { name: "Terra" }),
      "{arrowright}"
    );
    expect(screen.getByRole("radio", { name: "Terra" }).checked).toBe(true);
  });

  it("When pressing tab and arrow right two times it should check third radio button", () => {
    userEvent.tab();
    // This is currently the only way to trigger an arrow event. userEvent.keyboard('{ArrowRight}'); is not supported yet.
    userEvent.type(
      screen.getByRole("radio", { name: "Terra" }),
      "{arrowright}"
    );
    userEvent.type(
      screen.getByRole("radio", { name: "Earth" }),
      "{arrowright}"
    );
    expect(screen.getByRole("radio", { name: "Earth" }).checked).toBe(true);
  });
});
