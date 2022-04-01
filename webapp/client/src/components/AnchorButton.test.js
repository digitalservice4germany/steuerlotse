import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AnchorButton from "./AnchorButton";

const MOCK_PROPS = {
  text: "anchor text",
  url: "url/some/link/path",
  name: "name/some/link/path",
  isDownloadLink: false,
  isSecondaryButton: false,
  plausibleName: "plausibleName",
  className: "className",
  plausibleDomain: "domain/some/link/path",
};
const user = userEvent.setup();

describe("AnchorButton", () => {
  beforeEach(() => {
    render(<AnchorButton {...MOCK_PROPS} />);
  });

  it("should render the text", () => {
    expect(screen.getByText(MOCK_PROPS.text)).toBeInTheDocument();
  });

  it("should have a href attribute", () => {
    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.url)
    );
  });

  it("should not have a download attribute", () => {
    expect(screen.getByText(MOCK_PROPS.text).closest("a")).not.toHaveAttribute(
      "download"
    );
  });

  it("should run the plausible function on click button", async () => {
    window.plausible = jest.fn().mockReturnValue({ plausible: jest.fn() });

    await user.click(screen.getByText(MOCK_PROPS.text));

    expect(window.plausible).toHaveBeenCalledWith("plausibleName", undefined);
  });
});

describe("AnchorButton Download", () => {
  it("should have a download attribute", () => {
    const PROPS_DATA = { ...MOCK_PROPS, isDownloadLink: true };
    render(<AnchorButton {...PROPS_DATA} />);

    expect(screen.getByText(MOCK_PROPS.text).closest("a")).toHaveAttribute(
      "download"
    );
  });
});
