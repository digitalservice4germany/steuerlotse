import React from "react";
import { render, screen } from "@testing-library/react";
import TelephoneNumberPage from "./TelephoneNumberPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

let props = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    telephoneNumber: {
      value: "",
      errors: [],
    },
  },
  prevUrl: "/some/prev/path",
};

it("should render step header texts", () => {
  render(<TelephoneNumberPage {...props} />);
  expect(screen.getByText("Title")).toBeInTheDocument();
  expect(screen.getByText("Intro")).toBeInTheDocument();
});

it("should render field", () => {
  render(<TelephoneNumberPage {...props} />);
  expect(
    screen.getByLabelText("Telefonnummer", { exact: false })
  ).toBeInTheDocument();
});

it("should show optional text", () => {
  render(<TelephoneNumberPage {...props} />);
  expect(screen.getByText("optional")).toBeInTheDocument();
});

it("should link to the previous page", () => {
  render(<TelephoneNumberPage {...props} />);
  expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
    "href",
    expect.stringContaining("/some/prev/path")
  );
});
