import React from "react";
import { render } from "@testing-library/react";
import StepForm from "./StepForm";

it("should include the csrf token", () => {
  const { container } = render(<StepForm csrfToken="123abc" />);
  const hiddenInput = container.querySelector(
    'input[type="hidden"][name="csrf_token"]'
  );
  expect(hiddenInput).toBeInTheDocument();
  expect(hiddenInput.value).toEqual("123abc");
});
