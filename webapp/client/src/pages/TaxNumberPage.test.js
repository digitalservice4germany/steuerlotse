import React from "react";
import { render, screen } from "@testing-library/react";
import { fireEvent } from "@testing-library/dom";
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
    };
    render(<TaxNumberPage {...props} />);
  });

  it("Should show question for tax number", () => {
    expect(
      screen.queryByText(
        "Haben Sie bereits eine Steuernummer",
        notExactQueryOptions
      )
    ).not.toBeNull();
    expect(screen.queryByText("Ja")).not.toBeNull();
    expect(screen.queryByText("Nein")).not.toBeNull();
  });

  it("Should not show state selection", () => {
    expect(
      screen.queryByLabelText("Bundesland", notExactQueryOptions)
    ).toBeNull();
  });

  it("Should not show tax number input", () => {
    expect(screen.queryByText("Steuernummer")).toBeNull();
  });

  it("Should not show tax office selection", () => {
    expect(
      screen.queryByLabelText("Wählen Sie Ihr Finanzamt", notExactQueryOptions)
    ).toBeNull();
  });

  it("Should not show confirmation field", () => {
    expect(
      screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
    ).toBeNull();
  });

  describe("Select tax number", () => {
    beforeEach(() => {
      fireEvent.click(screen.getByText("Ja"));
    });

    it("Should show question for tax number", () => {
      expect(
        screen.queryByText(
          "Haben Sie bereits eine Steuernummer",
          notExactQueryOptions
        )
      ).not.toBeNull();
      expect(screen.queryByText("Ja")).not.toBeNull();
      expect(screen.queryByText("Nein")).not.toBeNull();
    });

    it("Should show state selection", () => {
      expect(
        screen.queryByLabelText("Bundesland", notExactQueryOptions)
      ).not.toBeNull();
      expect(screen.queryByRole("combobox")).not.toBeNull();
    });

    it("Should not show tax number input", () => {
      expect(screen.queryByText("Steuernummer")).toBeNull();
    });

    it("Should not show tax office selection", () => {
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

    describe("Select Baden-Württemberg", () => {
      beforeEach(() => {
        userEvent.selectOptions(screen.getByRole("combobox"), ["bw"]);
      });

      it("Should show question for tax number", () => {
        expect(
          screen.queryByText(
            "Haben Sie bereits eine Steuernummer",
            notExactQueryOptions
          )
        ).not.toBeNull();
        expect(screen.queryByText("Ja")).not.toBeNull();
        expect(screen.queryByText("Nein")).not.toBeNull();
      });

      it("Should show state selection with correct selected value", () => {
        expect(
          screen.queryByLabelText("Bundesland", notExactQueryOptions)
        ).not.toBeNull();
        expect(screen.queryAllByRole("combobox")[0]).toHaveValue("bw");
      });

      it("Should show split tax number input", () => {
        expect(screen.queryByText("Steuernummer")).not.toBeNull();
        expect(screen.queryAllByRole("textbox")).toHaveLength(3);
      });

      it("Should not show tax office selection", () => {
        expect(
          screen.queryByLabelText(
            "Wählen Sie Ihr Finanzamt",
            notExactQueryOptions
          )
        ).toBeNull();
      });

      it("Do not show confirmation field", () => {
        expect(
          screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
        ).toBeNull();
      });

      describe("Enter tax number and then toggle tax number available question", () => {
        beforeEach(() => {
          userEvent.type(screen.queryAllByRole("textbox")[0], "123");
          fireEvent.click(screen.getByText("Nein"));
          fireEvent.click(screen.getByText("Ja"));
        });

        it("Should show Bundesland with Baden-Württemberg selected", () => {
          expect(
            screen.queryByLabelText("Bundesland", notExactQueryOptions)
          ).not.toBeNull();
          expect(screen.queryAllByRole("combobox")[0]).toHaveValue("bw");
        });

        it("Tax number inputs are empty", () => {
          expect(screen.queryAllByRole("textbox")[0]).not.toHaveValue();
          expect(screen.queryAllByRole("textbox")[1]).not.toHaveValue();
          expect(screen.queryAllByRole("textbox")[2]).not.toHaveValue();
        });
      });
    });

    describe("Select Hessen", () => {
      beforeEach(() => {
        userEvent.selectOptions(screen.getByRole("combobox"), ["he"]);
      });

      it("Should show not split tax number input", () => {
        expect(screen.queryByText("Steuernummer")).not.toBeNull();
        expect(screen.queryAllByRole("textbox")).toHaveLength(1);
      });

      it("Should not show tax office selection", () => {
        expect(
          screen.queryByLabelText(
            "Wählen Sie Ihr Finanzamt",
            notExactQueryOptions
          )
        ).toBeNull();
      });

      it("Do not show confirmation field", () => {
        expect(
          screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
        ).toBeNull();
      });

      describe("Enter text and change state to Bayern", () => {
        beforeEach(() => {
          userEvent.type(screen.queryAllByRole("textbox")[0], "1234");
          userEvent.selectOptions(screen.getByRole("combobox"), ["by"]);
        });

        it("Should show split tax number input", () => {
          expect(screen.queryByText("Steuernummer")).not.toBeNull();
          expect(screen.queryAllByRole("textbox")).toHaveLength(3);
        });

        it("Tax number inputs are empty", () => {
          expect(screen.queryAllByRole("textbox")[0]).not.toHaveValue();
          expect(screen.queryAllByRole("textbox")[1]).not.toHaveValue();
          expect(screen.queryAllByRole("textbox")[2]).not.toHaveValue();
        });
      });
    });
  });

  describe("Select no tax number", () => {
    beforeEach(() => {
      fireEvent.click(screen.getByText("Nein"));
    });

    it("Should show question for tax number", () => {
      expect(
        screen.queryByText(
          "Haben Sie bereits eine Steuernummer",
          notExactQueryOptions
        )
      ).not.toBeNull();
      expect(screen.queryByText("Ja")).not.toBeNull();
      expect(screen.queryByText("Nein")).not.toBeNull();
    });

    it("Should show state selection", () => {
      expect(
        screen.queryByLabelText("Bundesland", notExactQueryOptions)
      ).not.toBeNull();
      expect(screen.queryByRole("combobox")).not.toBeNull();
    });

    it("Do not show tax number input", () => {
      expect(screen.queryByText("Steuernummer")).toBeNull();
    });

    it("Do not show tax office selection", () => {
      expect(
        screen.queryByLabelText(
          "Wählen Sie Ihr Finanzamt",
          notExactQueryOptions
        )
      ).toBeNull();
    });

    it("Do not show confirmation field", () => {
      expect(
        screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
      ).toBeNull();
    });

    describe("Select Baden-Württemberg", () => {
      beforeEach(() => {
        userEvent.selectOptions(
          screen.getByLabelText("Bundesland", notExactQueryOptions),
          ["bw"]
        );
      });

      it("Should show question for tax number", () => {
        expect(
          screen.queryByText(
            "Haben Sie bereits eine Steuernummer",
            notExactQueryOptions
          )
        ).not.toBeNull();
        expect(screen.queryByText("Ja")).not.toBeNull();
        expect(screen.queryByText("Nein")).not.toBeNull();
      });

      it("Should show state selection with correct selected value", () => {
        expect(
          screen.queryByLabelText("Bundesland", notExactQueryOptions)
        ).not.toBeNull();
        expect(screen.queryAllByRole("combobox")[0]).toHaveValue("bw");
      });

      it("Do not show tax number input", () => {
        expect(screen.queryByText("Steuernummer")).toBeNull();
      });

      it("Should show tax office selection", () => {
        expect(
          screen.queryByLabelText(
            "Wählen Sie Ihr Finanzamt",
            notExactQueryOptions
          )
        ).not.toBeNull();
      });

      it("Should not show confirmation field", () => {
        expect(
          screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
        ).toBeNull();
      });

      describe("Select tax office", () => {
        beforeEach(() => {
          userEvent.selectOptions(
            screen.getByLabelText("Finanzamt", notExactQueryOptions),
            ["2801"]
          );
        });

        it("Should show question for tax number", () => {
          expect(
            screen.queryByText(
              "Haben Sie bereits eine Steuernummer",
              notExactQueryOptions
            )
          ).not.toBeNull();
          expect(screen.queryByText("Ja")).not.toBeNull();
          expect(screen.queryByText("Nein")).not.toBeNull();
        });

        it("Should show state selection with correct selected value", () => {
          expect(
            screen.queryByLabelText("Bundesland", notExactQueryOptions)
          ).not.toBeNull();
          expect(screen.queryAllByRole("combobox")[0]).toHaveValue("bw");
        });

        it("Should not show tax number input", () => {
          expect(screen.queryByText("Steuernummer")).toBeNull();
        });

        it("Should show tax office selection", () => {
          expect(
            screen.queryByLabelText(
              "Wählen Sie Ihr Finanzamt",
              notExactQueryOptions
            )
          ).not.toBeNull();
        });

        it("Should show confirmation field", () => {
          expect(
            screen.queryByLabelText("Hiermit bestätige", notExactQueryOptions)
          ).not.toBeNull();
        });
      });
    });
  });
});

describe("TaxNumberPage with tax number set", () => {
  let props;
  const taxNumber = "12345678910";

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
          selectedValue: "bw",
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
          value: [taxNumber],
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
    };
    render(<TaxNumberPage {...props} />);
  });

  it("Should show keep tax number if state changes", () => {
    userEvent.selectOptions(screen.getByRole("combobox"), ["by"]);
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
