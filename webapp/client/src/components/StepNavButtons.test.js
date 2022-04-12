import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import StepNavButtons from "./StepNavButtons";

function setup(optionalProps) {
  const utils = render(<StepNavButtons {...optionalProps} />);
  const user = userEvent.setup();

  return { ...utils, user };
}

describe("StepNavButtons", () => {
  it("should render a button with the default button text", () => {
    setup();

    expect(screen.getByText(/Weiter/)).toBeInTheDocument();
    expect(screen.getByText(/Weiter/).tagName).toEqual("BUTTON");
  });

  it("should render a button with a custom button text", () => {
    setup({
      nextButtonLabel: "neeeeeext",
    });

    expect(screen.getByText(/neeeeeext/)).toBeInTheDocument();
    expect(screen.queryByText(/Weiter/)).not.toBeInTheDocument();
  });

  it("should not render an overview link", () => {
    setup();

    expect(screen.queryByText(/Zurück zur Übersicht/)).not.toBeInTheDocument();
  });

  it("should render a button to go to the overview if showOverviewButton is true", () => {
    setup({
      showOverviewButton: true,
    });

    expect(screen.getByText(/Zurück zur Übersicht/)).toBeInTheDocument();
    expect(screen.getByText(/Zurück zur Übersicht/).tagName).toEqual("BUTTON");
  });

  it("should not call plausible on showOverviewButton click without domain given", async () => {
    const { user } = setup({
      showOverviewButton: true,
      plausibleGoal: "plausible_goal",
    });

    window.plausible = jest.fn();

    await user.click(screen.getByText(/Zurück zur Übersicht/));

    expect(window.plausible).not.toHaveBeenCalled();
  });

  it("should call plausible on showOverviewButton click with default goal", async () => {
    const { user } = setup({
      showOverviewButton: true,
      plausibleDomain: "domain/some/link/path",
    });
    const EXPECTED_PLAUSIBLE_GOAL = "Zurück zur Übersicht";

    window.plausible = jest.fn();

    await user.click(screen.getByText(/Zurück zur Übersicht/));

    expect(window.plausible).toHaveBeenCalledWith(EXPECTED_PLAUSIBLE_GOAL, {
      props: undefined,
    });
  });

  it("should call plausible on showOverviewButton click with custom goal", async () => {
    const { user } = setup({
      showOverviewButton: true,
      plausibleDomain: "domain/some/link/path",
      plausibleGoal: "plausible_goal",
    });
    const EXPECTED_PLAUSIBLE_GOAL = "plausible_goal";

    window.plausible = jest.fn();

    await user.click(screen.getByText(/Zurück zur Übersicht/));

    expect(window.plausible).toHaveBeenCalledWith(EXPECTED_PLAUSIBLE_GOAL, {
      props: undefined,
    });
  });

  it("should call plausible on showOverviewButton click with goal and props", async () => {
    const { user } = setup({
      showOverviewButton: true,
      plausibleDomain: "domain/some/link/path",
      plausibleGoal: "plausible_goal",
      plausibleProps: { method: "plausible_props" },
    });
    const EXPECTED_PLAUSIBLE_GOAL = "plausible_goal";
    const EXPECTED_PLAUSIBLE_PROPS = { props: { method: "plausible_props" } };

    window.plausible = jest.fn();

    await user.click(screen.getByText(/Zurück zur Übersicht/));

    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });

  it("should render an explanatory button text", () => {
    setup({
      explanatoryButtonText: "some text",
    });

    expect(screen.getByText(/some text/)).toBeInTheDocument();
  });
});
