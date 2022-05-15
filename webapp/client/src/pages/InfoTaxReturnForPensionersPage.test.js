import React from "react";
import { render } from "@testing-library/react";
import InfoTaxReturnForPensionersPage from "./InfoTaxReturnForPensionersPage";

jest.mock("../components/ContentPageBox", () => ({
  __esModule: true,
  default: function ContentPageBox() {
    return <div>Content Page Box</div>;
  },
}));

jest.mock("../components/SuccessStepsInfoBox", () => ({
  __esModule: true,
  default: function SuccessStepsInfoBox() {
    return <div>Steps Info Box</div>;
  },
}));

function setup() {
  const MOCK_PROPS = {
    plausibleDomain: "/plausibleDomain/path",
  };
  const utils = render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);

  return { ...utils };
}

describe("InfoTaxReturnForPensionersPage", () => {
  it("should render the InfoTaxReturnForPensionersPage component", () => {
    setup();
  });
});
