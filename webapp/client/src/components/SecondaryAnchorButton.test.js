import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SecondaryAnchorButton from "./SecondaryAnchorButton";

describe("SecondaryAnchorButton", () => {
  const MOCK_PROPS = {
    text: "anchor text",
    url: "url/some/link/path",
    name: "name/some/link/path",
    isDownloadLink: false,
    plausibleName: "plausibleName",
    className: "className",
    plausibleDomain: "domain/some/link/path",
  };

  it("should render the text", () => {
    render(<SecondaryAnchorButton {...MOCK_PROPS} />);
    expect(screen.getByText(MOCK_PROPS.text)).toBeInTheDocument();
  });

  it("should have a href attribute", () => {
    render(<SecondaryAnchorButton {...MOCK_PROPS} />);
    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.url)
    );
  });

  it("should not have a download attribute", () => {
    const PROPS_DATA = { ...MOCK_PROPS, isDownloadLink: false };
    render(<SecondaryAnchorButton {...PROPS_DATA} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).not.toHaveAttribute(
      "download"
    );
  });

  it("should have a download attribute", () => {
    const PROPS_DATA = { ...MOCK_PROPS, isDownloadLink: true };
    render(<SecondaryAnchorButton {...PROPS_DATA} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "download"
    );
  });
});

describe("Secondary Button add plausible", () => {
  const MOCK_PROPS = {
    text: "anchor text",
    url: "url/some/link/path",
    name: "name/some/link/path",
    plausibleDomain: "domain/some/link/path",
    plausibleName: "plausible_name",
  };

  it("should run the plausible function on click button", async () => {
    const user = userEvent.setup();

    window.plausible = jest.fn();
    render(<SecondaryAnchorButton {...MOCK_PROPS} />);

    await user.click(screen.getByText(MOCK_PROPS.text));

    expect(window.plausible).toHaveBeenCalledWith("plausible_name", undefined);
  });
});
