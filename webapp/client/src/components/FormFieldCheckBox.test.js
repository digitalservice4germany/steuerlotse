import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldCheckBox from "./FormFieldCheckBox";

describe("When FormFieldCheckBox with default values", () => {
  let props;
  const user = userEvent.setup();

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      labelText: "foo",
      errors: [],
    };
    render(<FormFieldCheckBox {...props} />);
  });

  it("Should show checkBox", () => {
    expect(screen.getByRole("checkbox")).toBeTruthy();
  });

  it("Should show label", () => {
    expect(screen.getByRole("checkbox")).toBeTruthy();
  });

  it("Should not preselect checkBox", () => {
    expect(screen.getByLabelText("foo")).not.toBeChecked();
  });

  it("Should select checkBox on click", async () => {
    await user.click(screen.getByLabelText("foo"));

    expect(screen.getByLabelText("foo")).toBeChecked();
  });

  it("Should focus checkBox when using tab", async () => {
    await user.tab();

    expect(screen.getByLabelText("foo")).toHaveFocus();
  });

  it("Should select checkBox when using tab and pressing space", async () => {
    await user.tab();
    await user.keyboard(" ");

    expect(screen.getByLabelText("foo")).toBeChecked();
  });

  it("Should deselect checkBox when using tab and pressing space twice", async () => {
    await user.tab();
    await user.keyboard(" ");
    await user.keyboard(" ");

    expect(screen.getByLabelText("foo")).not.toBeChecked();
  });
});

describe("When preselected FormFieldCheckBox", () => {
  let props;

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      labelText: "foo",
      errors: [],
      checked: true,
    };
    render(<FormFieldCheckBox {...props} />);
  });

  it("Should show checkBox", () => {
    expect(screen.getByRole("checkbox")).toBeTruthy();
  });

  it("Should show selected checkBox", () => {
    expect(screen.getByLabelText("foo")).toBeChecked();
  });
});

describe("When FormFieldCheckBox with errors", () => {
  let props;

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      labelText: "foo",
      errors: ["fooError1", "fooError2"],
    };
    render(<FormFieldCheckBox {...props} />);
  });

  it("Should show errors", () => {
    expect(screen.getByText("fooError1")).toBeTruthy();
    expect(screen.getByText("fooError2")).toBeTruthy();
  });
});
