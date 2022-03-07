import React from "react";
import { render, screen } from "@testing-library/react";
import DownloadLink from "./DownloadLink";

describe("Download link", () => {
  beforeEach(() => {
    render(<DownloadLink text="Download" url="/some/path" />);
  });

  it("should render the download link text", () => {
    expect(screen.getByText("Download")).toBeInTheDocument();
  });

  it("should link to the URL", () => {
    expect(screen.getByText("Download").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/path")
    );
  });
});
