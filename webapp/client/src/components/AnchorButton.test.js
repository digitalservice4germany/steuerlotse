import React from "react";
import { render, screen } from "@testing-library/react";
import AnchorButton from "./AnchorButton";

const MOCK_PROPS = {
  text: "anchor text",
  url: "/some/link/path",
  name: "/some/link/path",
  isDownloadLink: "/some/link/path",
  isSecondaryButton: "/some/link/path",
  plausibleName: "/some/link/path",
  className: "/some/link/path",
  plausibleDomain: "/some/link/path",
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

  it("should not have a download attribute", () => {
    const PROPS_DATA = { ...MOCK_PROPS, isDownloadLink: false };
    render(<AnchorButton {...PROPS_DATA} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).not.toHaveAttribute(
      "download"
    );
  });

  it("should have a download attribute", () => {
    const PROPS_DATA = { ...MOCK_PROPS, isDownloadLink: true };
    render(<AnchorButton {...PROPS_DATA} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "download"
    );
  });
});
