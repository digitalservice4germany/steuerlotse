import React from "react";

import TaxNumberPage from "../pages/TaxNumberPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/TaxNumberPage",
  component: TaxNumberPage,
};

function Template(args) {
  <TaxNumberPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Steuernummer",
    intro:
      "Die Steuernummer wird Ihnen vom zuständigen Finanzamt zugeteilt – dort, wo sich Ihr Wohnsitz befindet. Sie erhalten jeweils eine andere Steuernummer, wenn sich Ihre Lebenssituation ändert. Gründe können beispielsweise ein Umzug, eine Heirat oder die Änderung der Veranlagungsart sein.",
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
      selectedValue: undefined,
      options: [
        { value: "bw", displayName: "Baden-Württemberg" },
        { value: "by", displayName: "Bayern" },
        { value: "he", displayName: "Hessen" },
      ],
      errors: [],
    },
    bufaNr: {
      selectedValue: undefined,
      errors: [],
    },
    steuernummer: {
      value: ["198", "1131", "0010"],
      errors: [],
    },
    requestNewTaxNumber: {
      checked: true,
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
  prevUrl: "FooWebsite",
};

export const MultipleUsers = Template.bind({});
MultipleUsers.args = {
  ...Default.args,
  numberOfUsers: 2,
};

export const NoTaxNumber = Template.bind({});
NoTaxNumber.args = {
  ...Default.args,
  fields: {
    steuernummerExists: {
      value: "no",
      errors: [],
    },
    bundesland: {
      selectedValue: "by",
      options: [
        { value: "bw", displayName: "Baden-Württemberg" },
        { value: "by", displayName: "Bayern" },
        { value: "he", displayName: "Hessen" },
      ],
      errors: [],
    },
    bufaNr: {
      selectedValue: "9101",
      errors: [],
    },
    steuernummer: {
      value: [""],
      errors: [],
    },
    requestNewTaxNumber: {
      checked: true,
      errors: [],
    },
  },
};

export const NoTaxNumberAndErrors = Template.bind({});
NoTaxNumberAndErrors.args = {
  ...Default.args,
  fields: {
    steuernummerExists: {
      value: "no",
      errors: ["Diese Angabe fehlt."],
    },
    bundesland: {
      selectedValue: "by",
      options: [
        { value: "bw", displayName: "Baden-Württemberg" },
        { value: "by", displayName: "Bayern" },
        { value: "he", displayName: "Hessen" },
      ],
      errors: ["Diese Angabe fehlt."],
    },
    bufaNr: {
      selectedValue: "9101",
      errors: ["Diese Angabe fehlt."],
    },
    steuernummer: {
      value: [""],
      errors: [],
    },
    requestNewTaxNumber: {
      checked: true,
      errors: ["Diese Angabe fehlt."],
    },
  },
};

export const WithTaxNumber = Template.bind({});
WithTaxNumber.args = {
  ...Default.args,
  fields: {
    steuernummerExists: {
      value: "yes",
      errors: [],
    },
    bundesland: {
      selectedValue: "by",
      options: [
        { value: "bw", displayName: "Baden-Württemberg" },
        { value: "by", displayName: "Bayern" },
        { value: "he", displayName: "Hessen" },
      ],
      errors: [],
    },
    bufaNr: {
      selectedValue: undefined,
      errors: [],
    },
    steuernummer: {
      value: ["198", "1131", "0010"],
      errors: [],
    },
    requestNewTaxNumber: {
      checked: true,
      errors: [],
    },
  },
};

export const WithTaxNumberAndErrors = Template.bind({});
WithTaxNumberAndErrors.args = {
  ...Default.args,
  fields: {
    steuernummerExists: {
      value: "yes",
      errors: ["Diese Angabe fehlt."],
    },
    bundesland: {
      selectedValue: "by",
      options: [
        { value: "bw", displayName: "Baden-Württemberg" },
        { value: "by", displayName: "Bayern" },
        { value: "he", displayName: "Hessen" },
      ],
      errors: ["Diese Angabe fehlt."],
    },
    bufaNr: {
      selectedValue: undefined,
      errors: [],
    },
    steuernummer: {
      value: ["198", "1131", "0010"],
      errors: ["Diese Angabe fehlt."],
    },
    requestNewTaxNumber: {
      checked: undefined,
      errors: [],
    },
  },
};
