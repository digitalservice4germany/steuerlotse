import React from "react";
import { render } from "@testing-library/react";
import InfoTaxReturnForPensionersPage from "./InfoTaxReturnForPensionersPage";

const MOCK_PROPS = {
  plausibleDomain: "/plausibleDomain/path",
  url: "/eligibility/step/marital_status?link_overview=False",
  contactUsUrl: "mailto:kontakt@steuerlotse-rente.de",
  howItWorksLink: "/sofunktionierts",
};

describe("InfoTaxReturnForPensionersPage", () => {
  it("should render the InfoTaxReturnForPensionersPage component", () => {
    render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);
  });

  beforeEach(() => {
    render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);
  });
});
