import React from "react";

import RegistrationPage from "../pages/RegistrationPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/Registration",
  component: RegistrationPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <RegistrationPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Registrieren und persönlichen Freischaltcode beantragen",
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
  loginLink: "/unlock_code_activation/step/data_input",
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
      checked: false,
      errors: [],
    },
    registrationConfirmTermsOfService: {
      checked: false,
      errors: [],
    },
  },
};
