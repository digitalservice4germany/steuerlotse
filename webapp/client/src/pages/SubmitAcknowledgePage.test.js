import React from "react";
import { render, screen } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import i18n from "i18next";
import { fireEvent } from "@testing-library/dom";
import SubmitAcknowledgePage from "./SubmitAcknowledgePage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
  logoutUrl: "/some/link/path",
};

describe("SubmitAcknowledgePage", () => {
  beforeEach(() => {
    render(<SubmitAcknowledgePage {...MOCK_PROPS} />);
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });

  it("should link to logout in text", () => {
    expect(screen.getByText("Abmelden").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.logoutUrl)
    );
  });

  it("should render facebook icon", () => {
    expect(screen.getByLabelText("facebook")).toBeInTheDocument();
  });

  it("should render email icon", () => {
    expect(screen.getByLabelText("email")).toBeInTheDocument();
  });
});

describe("SubmitAcknowledgePage translations", () => {
  const submitAcknowledgeTexts =
    i18n.getDataByLanguage("de").translation.submitAcknowledge;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <SubmitAcknowledgePage {...MOCK_PROPS} />
      </I18nextProvider>
    );
  });

  it("should render step header texts", () => {
    expect(
      screen.getByText(submitAcknowledgeTexts.successMessage)
    ).toBeDefined();
  });

  it("should render next steps header", () => {
    expect(
      screen.getByText(submitAcknowledgeTexts["next-steps"].heading)
    ).toBeDefined();
  });

  it("should render next steps text", () => {
    expect(
      screen.getByText(submitAcknowledgeTexts["next-steps"].text)
    ).toBeDefined();
  });

  it("should render recommend header", () => {
    expect(
      screen.getByText(submitAcknowledgeTexts.recommend.heading)
    ).toBeDefined();
  });

  it("should render recommend text", () => {
    expect(
      screen.getByText(submitAcknowledgeTexts.recommend.text)
    ).toBeDefined();
  });

  it("should render logout header", () => {
    expect(
      screen.getByText(submitAcknowledgeTexts.logout.heading)
    ).toBeDefined();
  });

  it("should render logout text", () => {
    expect(screen.getByText(submitAcknowledgeTexts.logout.text)).toBeDefined();
  });
});

describe("SubmitAcknowledgePage with plausible domain", () => {
  const MOCK_PROPS_PLAUSIBLE = {
    prevUrl: "/some/prev/path",
    logoutUrl: "/some/link/path",
    plausibleDomain: "http://localhost:3000",
  };

  beforeEach(() => {
    window.plausible = jest.fn().mockReturnValue({ plausible: jest.fn() });
    render(<SubmitAcknowledgePage {...MOCK_PROPS_PLAUSIBLE} />);
  });

  it("should add plausible goal for facebook click", () => {
    fireEvent.click(screen.getByLabelText("facebook"));
    expect(window.plausible).toHaveBeenCalledWith("Facebook icon clicked", {
      method: "submitAcknowledge",
    });
  });

  it("should add plausible goal for email click", () => {
    fireEvent.click(screen.getByLabelText("email"));
    expect(window.plausible).toHaveBeenCalledWith("Email icon clicked", {
      method: "submitAcknowledge",
    });
  });
});
