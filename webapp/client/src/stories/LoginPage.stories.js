import React from "react";

import LoginPage from "../pages/LoginPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/Login",
  component: LoginPage,
};

const Template = (args) => <LoginPage {...args} />;

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Melden Sie sich mit Ihrem Freischaltcode an",
    intro:
      "Sie sind vorbereitet und haben den Freischaltcode per Post erhalten? Dann können Sie mit Ihrer Steuererklärung 2020 beginnen.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    idnr: {
      value: ["04", "452", "397", "687"],
      errors: [],
    },
    unlockCode: {
      value: ["DBNH", "B8JS", "9JE7"],
      errors: [],
    },
  },
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
    unlockCode: {
      value: ["xxxx", "abc", ""],
      errors: ["Ein gültiger Freischaltcode hat genau 12 Zeichen."],
    },
  },
};
