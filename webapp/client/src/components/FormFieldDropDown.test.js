import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldDropDown from "./FormFieldDropDown";

describe("FormFieldDropDown", () => {
  let props;
  const user = userEvent.setup();
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
      onChangeHandler,
    };
    render(<FormFieldDropDown {...props} />);
  });

  it("should select second option", async () => {
    await user.selectOptions(screen.getByRole("combobox"), ["B"]);

    expect(screen.getByRole("option", { name: "Vulcan" }).selected).toBe(false);
    expect(screen.getByRole("option", { name: "Terra" }).selected).toBe(true);
    expect(screen.getByRole("option", { name: "Earth" }).selected).toBe(false);
  });

  it("should call the change handler with B", async () => {
    await user.selectOptions(screen.getByRole("combobox"), ["B"]);

    expect(onChangeHandler).toHaveBeenCalled();

    const changeEvent = onChangeHandler.mock.calls[0][0];
    expect(changeEvent.target.value).toEqual("B");
  });

  it("should select third option", async () => {
    await user.selectOptions(screen.getByRole("combobox"), ["C"]);

    expect(screen.getByRole("option", { name: "Vulcan" }).selected).toBe(false);
    expect(screen.getByRole("option", { name: "Terra" }).selected).toBe(false);
    expect(screen.getByRole("option", { name: "Earth" }).selected).toBe(true);
  });

  it("should call the change handler with C", async () => {
    await user.selectOptions(screen.getByRole("combobox"), ["C"]);

    expect(onChangeHandler).toHaveBeenCalled();

    const changeEvent = onChangeHandler.mock.calls[0][0];
    expect(changeEvent.target.value).toEqual("C");
  });

  it("should set focus on dropDown when pressing tab", async () => {
    await user.tab();

    expect(screen.getByRole("combobox")).toHaveFocus();
  });

  it("should remove focus on dropDown when pressing tab two times", async () => {
    await user.tab();
    await user.tab();

    expect(screen.getByRole("combobox")).not.toHaveFocus();
  });
});
