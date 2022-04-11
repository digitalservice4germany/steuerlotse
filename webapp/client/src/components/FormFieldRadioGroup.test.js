import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { within } from "@testing-library/dom";
import FormFieldRadioGroup from "./FormFieldRadioGroup";

describe("FormFieldRadioGroup", () => {
  let props;
  const onChangeHandler = jest.fn();
  const user = userEvent.setup();

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
      onChangeHandler,
    };
    render(<FormFieldRadioGroup {...props} />);
  });

  it("correct input is selected, when label is clicked", async () => {
    await user.click(screen.getByText("Vulcan"));

    expect(screen.getByLabelText("Vulcan").checked).toEqual(true);
    expect(screen.getByLabelText("Terra").checked).toEqual(false);
    expect(screen.getByLabelText("Earth").checked).toEqual(false);
  });

  it("should only select second option", async () => {
    await user.click(screen.getByLabelText("Terra"));

    expect(screen.getByRole("radio", { name: "Vulcan" })).not.toBeChecked();
    expect(screen.getByRole("radio", { name: "Terra" })).toBeChecked();
    expect(screen.getByRole("radio", { name: "Earth" })).not.toBeChecked();
  });

  it("should call the change handler with B, when second option has been selected", async () => {
    await user.click(screen.getByLabelText("Terra"));

    expect(onChangeHandler).toHaveBeenCalled();

    const changeEvent = onChangeHandler.mock.calls[0][0];

    expect(changeEvent.target.value).toEqual("B");
  });

  it("should set focus on first radio button, when pressing tab", async () => {
    await user.tab();

    expect(screen.getByRole("radio", { name: "Vulcan" })).toHaveFocus();
  });

  it("should remove focus from all radio buttons, when pressing tab two times", async () => {
    await user.tab();
    await user.tab();

    expect(screen.getByRole("radio", { name: "Vulcan" })).not.toHaveFocus();
    expect(screen.getByRole("radio", { name: "Terra" })).not.toHaveFocus();
    expect(screen.getByRole("radio", { name: "Earth" })).not.toHaveFocus();
  });
});

describe("FormFieldRadioGroup with errors", () => {
  let props;
  const onChangeHandler = jest.fn();

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
      },
      errors: ["Error!"],
      options: [
        { value: "A", displayName: "Vulcan" },
        { value: "B", displayName: "Terra" },
        { value: "C", displayName: "Earth" },
      ],
      onChangeHandler,
    };
    render(<FormFieldRadioGroup {...props} />);
  });

  it("should show error inside of fieldset", () => {
    const fieldset = screen.getByRole("group");
    expect(within(fieldset).getByText("Error!")).toBeTruthy();
  });

  it("should have autofocus on first radio button", () => {
    expect(screen.getByRole("radio", { name: "Vulcan" })).toHaveFocus();
  });
});
