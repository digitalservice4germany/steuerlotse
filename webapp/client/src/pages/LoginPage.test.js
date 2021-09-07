import { render, screen } from "@testing-library/react";
import LoginPage from "./LoginPage";

test("renders learn react link", () => {
  render(<LoginPage />);
  const element = screen.getByText(/Page content/i);
  expect(element).toBeInTheDocument();
  expect(element).not.toBeVisible();
});
