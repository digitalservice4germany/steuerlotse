import React from "react";

import RegistrationPage from "../pages/RegistrationPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/Registration",
  component: RegistrationPage,
};

const Template = (args) => <RegistrationPage {...args} />;

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Registrieren und persönlichen Freischaltcode beantragen",
    intro:
      "Mit Ihrer Registrierung beantragen Sie einen Freischaltcode bei Ihrer Finanzverwaltung. Sie erhalten diesen mit einem Brief wenige Tage nach erfolgreicher Beantragung. Wenn Sie die Zusammenveranlagung nutzen möchten, muss sich nur eine Person registrieren.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    idnr: {
      value: ["04", "452", "397", "687"],
      errors: [],
    },
    dob: {
      value: ["01", "01", "1985"],
      errors: [],
    },
    registrationConfirmDataPrivacy: {
      errors: [],
    },
    registrationConfirmTermsOfService: {
      errors: [],
    },
    registrationConfirmIncomes: {
      errors: [],
    },
    registrationConfirmEData: {
      errors: [],
    },
  },
  eligibilityLink: "/eligibility/start",
  termsOfServiceLink: "/agb",
  dataPrivacyLink: "/datenschutz",
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  fields: {
    ...Default.args.fields,
    idnr: {
      value: ["12", "345", "678", "90"],
      errors: ["Geben Sie bitte eine gültige Steuer-Identifikationsnummer an."],
    },
    dob: {
      value: ["40", "01", "1985"],
      errors: ["Geben Sie ein gültiges Datum an."],
    },
    registrationConfirmDataPrivacy: {
      value: false,
      errors: [],
    },
    registrationConfirmTermsOfService: {
      value: false,
      errors: [],
    },
  },
};
