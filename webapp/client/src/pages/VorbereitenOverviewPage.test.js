import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import VorbereitenOverviewPage from "./VorbereitenOverviewPage";

const REQUIRED_PROPS = {
  downloadPreparationLink: "downloadPreparationLink",
  vorsorgeaufwendungenUrl: "vorsorgeaufwendungenUrl",
  krankheitskostenUrl: "krankheitskostenUrl",
  pflegekostenUrl: "pflegekostenUrl",
  angabenBeiBehinderungUrl: "angabenBeiBehinderungUrl",
  bestattungskostenUrl: "bestattungskostenUrl",
  wiederbeschaffungskostenUrl: "wiederbeschaffungskostenUrl",
  haushaltsnaheDienstleistungenUrl: "haushaltsnaheDienstleistungenUrl",
  handwerkerleistungenUrl: "handwerkerleistungenUrl",
  spendenUndMitgliedsbeitraegeUrl: "spendenUndMitgliedsbeitraegeUrl",
  kirchensteuerUrl: "kirchensteuerUrl",
};

function setup(optionalProps) {
  const utils = render(
    <VorbereitenOverviewPage {...REQUIRED_PROPS} {...optionalProps} />
  );
  const downloadButton = screen.getByText("Vorbereitungshilfe speichern [PDF]");
  const buttonVorsorgeaufwendungen = screen.getByText("Vorsorgeaufwendungen");
  const buttonKrankheitskosten = screen.getByText("Krankheitskosten");
  const buttonPflegekosten = screen.getByText("Pflegekosten");
  const buttonAngabenBeiBehinderung = screen.getByText(
    "Angaben bei Behinderung"
  );
  const buttonBestattungskosten = screen.getByText("Bestattungskosten");
  const buttonWiederbeschaffungskosten = screen.getByText(
    "Wiederbeschaffungskosten"
  );
  const buttonHaushaltsnaheDienstleistungen = screen.getByText(
    "Haushaltsnahe Dienstleistungen"
  );
  const buttonHandwerkerleistungen = screen.getByText("Handwerkerleistungen");
  const buttonSpendenUndMitgliedsbeiträge = screen.getByText(
    "Spenden und Mitgliedsbeiträge"
  );
  const buttonKirchensteuer = screen.getByText("Kirchensteuer");
  const user = userEvent.setup();

  return {
    ...utils,
    downloadButton,
    buttonVorsorgeaufwendungen,
    buttonKrankheitskosten,
    buttonPflegekosten,
    buttonAngabenBeiBehinderung,
    buttonBestattungskosten,
    buttonWiederbeschaffungskosten,
    buttonHaushaltsnaheDienstleistungen,
    buttonHandwerkerleistungen,
    buttonSpendenUndMitgliedsbeiträge,
    buttonKirchensteuer,
    user,
  };
}

describe("UnlockCodeSuccessPage", () => {
  it("should link to Vorsorgeaufwendungen", () => {
    const { buttonVorsorgeaufwendungen } = setup();

    expect(buttonVorsorgeaufwendungen.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.vorsorgeaufwendungenUrl)
    );
  });

  it("should link to Krankheitskosten", () => {
    const { buttonKrankheitskosten } = setup();

    expect(buttonKrankheitskosten.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.krankheitskostenUrl)
    );
  });

  it("should link to Pflegekosten", () => {
    const { buttonPflegekosten } = setup();

    expect(buttonPflegekosten.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.pflegekostenUrl)
    );
  });

  it("should link to Angaben bei Behinderung", () => {
    const { buttonAngabenBeiBehinderung } = setup();

    expect(buttonAngabenBeiBehinderung.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.angabenBeiBehinderungUrl)
    );
  });

  it("should link to Bestattungskosten", () => {
    const { buttonBestattungskosten } = setup();

    expect(buttonBestattungskosten.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.bestattungskostenUrl)
    );
  });

  it("should link to Wiederbeschaffungskosten", () => {
    const { buttonWiederbeschaffungskosten } = setup();

    expect(buttonWiederbeschaffungskosten.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.wiederbeschaffungskostenUrl)
    );
  });

  it("should link to Haushaltsnahe Dienstleistungen", () => {
    const { buttonHaushaltsnaheDienstleistungen } = setup();

    expect(buttonHaushaltsnaheDienstleistungen.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.haushaltsnaheDienstleistungenUrl)
    );
  });

  it("should link to Handwerkerleistungen", () => {
    const { buttonHandwerkerleistungen } = setup();

    expect(buttonHandwerkerleistungen.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.handwerkerleistungenUrl)
    );
  });

  it("should link to Spenden und Mitgliedsbeiträge", () => {
    const { buttonSpendenUndMitgliedsbeiträge } = setup();

    expect(buttonSpendenUndMitgliedsbeiträge.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.spendenUndMitgliedsbeitraegeUrl)
    );
  });

  it("should link to Kirchensteuer", () => {
    const { buttonKirchensteuer } = setup();

    expect(buttonKirchensteuer.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.kirchensteuerUrl)
    );
  });
});
