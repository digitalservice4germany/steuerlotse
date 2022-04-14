import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaxNumberPage from "./TaxNumberPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

const notExactQueryOptions = { exact: false };

describe("TaxNumberPage", () => {
  let props;

  beforeEach(() => {
    props = {
      stepHeader: {
        title: "fooTitle",
        intro: "fooIntro",
      },
      form: {
        ...StepFormDefault.args,
      },
      fields: {
        steuernummerExists: {
          value: undefined,
          errors: [],
        },
        bundesland: {
          options: [
            { value: "bw", displayName: "Baden-Württemberg" },
            { value: "by", displayName: "Bayern" },
            { value: "he", displayName: "Hessen" },
          ],
          errors: [],
        },
        bufaNr: {
          options: [],
          errors: [],
        },
        steuernummer: {
          value: [],
          errors: [],
        },
        requestNewTaxNumber: {
          errors: [],
        },
      },
      taxOfficeList: [
        {
          stateAbbreviation: "bw",
          name: "Baden-Württemberg",
          taxOffices: [
            { name: "Finanzamt Villingen-Schwenningen", bufaNr: "2801" },
          ],
        },
        {
          stateAbbreviation: "by",
          name: "Bayern",
          taxOffices: [
            {
              name: "Finanzamt München Arbeitnehmerbereich (101)",
              bufaNr: "9101",
            },
            {
              name: "Finanzamt München Arbeitgeberbereich (102)",
              bufaNr: "9102",
            },
          ],
        },
        {
          stateAbbreviation: "he",
          name: "Hessen",
          taxOffices: [
            { name: "Finanzamt Hessen 1", bufaNr: "2250" },
            { name: "Finanzamt Hessen 2", bufaNr: "2251" },
          ],
        },
      ],
      numberOfUsers: 1,
      prevUrl: "fooUrl",
    };
    render(<TaxNumberPage {...props} />);
  });

  describe("TaxNumberPage default without user selection", () => {
    it("should show question for tax number", () => {
      expect(
        screen.queryByText(
          "Haben Sie bereits eine Steuernummer",
          notExactQueryOptions
        )
      ).not.toBeNull();
      expect(screen.queryByText("Ja")).not.toBeNull();
      expect(screen.queryByText("Nein")).not.toBeNull();
    });

    it("should not show state selection", () => {
      expect(
        screen.queryByLabelText("Bundesland", notExactQueryOptions)
      ).toBeNull();
    });

    it("should not show tax number input", () => {
      expect(screen.queryByText("Steuernummer")).toBeNull();
    });

    it("should not show tax office selection", () => {
      expect(
        screen.queryByLabelText(
          "Wählen Sie Ihr Finanzamt",
          notExactQueryOptions
        )
      ).toBeNull();
    });

    it("should not show confirmation field", () => {
      expect(
        screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
      ).toBeNull();
    });
  });

  describe("TaxNumberPage if user has a tax number", () => {
    const user = userEvent.setup();

    it("should show question for tax number", () => {
      expect(
        screen.queryByText(
          "Haben Sie bereits eine Steuernummer",
          notExactQueryOptions
        )
      ).not.toBeNull();
      expect(screen.queryByText("Ja")).not.toBeNull();
      expect(screen.queryByText("Nein")).not.toBeNull();
    });

    it("should show state selection", async () => {
      await user.click(screen.getByText("Ja"));

      expect(
        screen.queryByLabelText("Bundesland", notExactQueryOptions)
      ).not.toBeNull();
      expect(screen.queryByRole("combobox")).not.toBeNull();
    });

    it("should not show tax number input", () => {
      expect(screen.queryByText("Steuernummer")).toBeNull();
    });

    it("should not show tax office selection", () => {
      expect(
        screen.queryByLabelText(
          "Wählen Sie Ihr Finanzamt",
          notExactQueryOptions
        )
      ).toBeNull();
    });

    it("Should not show confirmation field", () => {
      expect(
        screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
      ).toBeNull();
    });
  });

  describe("TaxNumberPage if user does not have a tax number", () => {
    const user = userEvent.setup();

    it("should show question for tax number", () => {
      expect(
        screen.queryByText(
          "Haben Sie bereits eine Steuernummer",
          notExactQueryOptions
        )
      ).not.toBeNull();
      expect(screen.queryByText("Ja")).not.toBeNull();
      expect(screen.queryByText("Nein")).not.toBeNull();
    });

    it("should show state selection", async () => {
      await user.click(screen.getByText("Nein"));

      expect(
        screen.queryByLabelText("Bundesland", notExactQueryOptions)
      ).not.toBeNull();
      expect(screen.queryByRole("combobox")).not.toBeNull();
    });

    it("does not show tax number input", () => {
      expect(screen.queryByText("Steuernummer")).toBeNull();
    });

    it("does not show tax office selection", () => {
      expect(
        screen.queryByLabelText(
          "Wählen Sie Ihr Finanzamt",
          notExactQueryOptions
        )
      ).toBeNull();
    });

    it("does not show confirmation field", () => {
      expect(
        screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
      ).toBeNull();
    });
  });
});

describe("TaxNumberPage with tax number set", () => {
  let props;
  const taxNumber = "12345678910";
  const user = userEvent.setup();

  beforeEach(() => {
    props = {
      stepHeader: {
        title: "fooTitle",
        intro: "fooIntro",
      },
      form: {
        ...StepFormDefault.args,
      },
      fields: {
        steuernummerExists: {
          value: "yes",
          errors: [],
        },
        bundesland: {
          selectedValue: "nw",
          options: [
            { value: "nw", displayName: "Nordrhein-Westfalen" },
            { value: "by", displayName: "Bayern" },
            { value: "he", displayName: "Hessen" },
          ],
          errors: [],
        },
        bufaNr: {
          options: [],
          errors: [],
        },
        steuernummer: {
          value: [taxNumber],
          errors: [],
        },
        requestNewTaxNumber: {
          errors: [],
        },
      },
      taxOfficeList: [
        {
          stateAbbreviation: "nw",
          name: "Nordrhein-Westfalen",
          taxOffices: [{ name: "Köln", bufaNr: "5215" }],
        },
        {
          stateAbbreviation: "by",
          name: "Bayern",
          taxOffices: [
            {
              name: "Finanzamt München Arbeitnehmerbereich (101)",
              bufaNr: "9101",
            },
            {
              name: "Finanzamt München Arbeitgeberbereich (102)",
              bufaNr: "9102",
            },
          ],
        },
        {
          stateAbbreviation: "he",
          name: "Hessen",
          taxOffices: [
            { name: "Finanzamt Hessen 1", bufaNr: "2250" },
            { name: "Finanzamt Hessen 2", bufaNr: "2251" },
          ],
        },
      ],
      numberOfUsers: 1,
      prevUrl: "fooUrl",
    };
    render(<TaxNumberPage {...props} />);
  });

  it("Should enter the correct default values into the taxnumber inputs", () => {
    expect(screen.queryAllByRole("textbox")[0]).toHaveValue(
      taxNumber.slice(0, 3)
    );
    expect(screen.queryAllByRole("textbox")[1]).toHaveValue(
      taxNumber.slice(3, 7)
    );
    expect(screen.queryAllByRole("textbox")[2]).toHaveValue(
      taxNumber.slice(7, 11)
    );
  });

  it("Should show keep tax number if state changes", async () => {
    await user.selectOptions(screen.getByRole("combobox"), ["by"]);

    expect(screen.queryByText("Steuernummer")).not.toBeNull();
    expect(screen.queryAllByRole("textbox")).toHaveLength(3);
    expect(screen.queryAllByRole("textbox")[0]).toHaveValue(
      taxNumber.slice(0, 3)
    );
    expect(screen.queryAllByRole("textbox")[1]).toHaveValue(
      taxNumber.slice(3, 6)
    );
    expect(screen.queryAllByRole("textbox")[2]).toHaveValue(
      taxNumber.slice(6, 11)
    );
  });
});
