import React from "react";
import { render, screen } from "@testing-library/react";
import LogoutPage from "./LogoutPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

const MOCK_PROPS = {
  form: {
    ...StepFormDefault.args,
  },
};

const EXPECTED_HEADER = {
  title: "Sind Sie sicher, dass Sie sich abmelden möchten?",
  intro:
    "Ihre bisher eingetragenen Angaben werden erst an uns übermittelt, wenn Sie Ihre Steuererklärung verschicken. Ihre Steuererklärung wird daher nicht zwischengespeichert. Wenn Sie sich abmelden, kann es sein, dass Ihre Angaben bei der nächsten Anmeldung nicht mehr vorhanden sind.",
};

describe("LogoutPage", () => {
  beforeEach(() => {
    render(<LogoutPage {...MOCK_PROPS} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should render step intro text", () => {
    expect(screen.getByText(EXPECTED_HEADER.intro)).toBeInTheDocument();
  });

  it("should link to the next page", () => {
    expect(screen.getByText("Abmelden")).toBeInTheDocument();
  });
});
