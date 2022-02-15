import React from "react";
import { render, screen } from "@testing-library/react";
import ButtonLink from "./ButtonLink";

const MOCK_PROPS = {
  text: "anchor text",
  url: "/some/link/path",
};

describe("ButtonLink", () => {
  it("should render the text", () => {
    render(<ButtonLink {...MOCK_PROPS} />);

    expect(screen.getByText(MOCK_PROPS.text)).toBeInTheDocument();
    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.url)
    );
  });
});
