import React from "react";
import { render, screen } from "@testing-library/react";
import FailureMessageBox from "./FailureMessageBox";

describe("Display failure icon", () => {
  beforeEach(() => {
    render(<FailureMessageBox title="This is not my sandwich" />);
  });

  it("should render the download link text", () => {
    expect(screen.getByText("This is not my sandwich")).toBeInTheDocument();
  });

  it("should render red cross icon", () => {
    expect(screen.getByText("failure_icon.svg").closest("svg")).toHaveAttribute(
      "alt",
      expect.stringContaining("Weißes Kreuzzeichen auf rotem Kreis")
    );
  });
});
