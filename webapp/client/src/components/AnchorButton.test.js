import React from "react";
import { render, screen } from "@testing-library/react";
import AnchorButton from "./AnchorButton";

const MOCK_PROPS = {
  text: "anchor text",
  url: "/some/link/path",
  isDownloadLink: false,
};

describe("AnchorButton", () => {
  it("should render the text", () => {
    render(<AnchorButton {...MOCK_PROPS} />);

    expect(screen.getByText(MOCK_PROPS.text)).toBeInTheDocument();
    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.url)
    );
  });

  it("should not has a download attribute", () => {
    render(<AnchorButton {...MOCK_PROPS} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).not.toHaveAttribute(
      "download"
    );
  });

  it("should has a download attribute", () => {
    MOCK_PROPS.isDownloadLink = true;
    render(<AnchorButton {...MOCK_PROPS} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "download"
    );
  });
});
