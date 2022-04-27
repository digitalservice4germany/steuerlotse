import React from "react";

import RevocationPage from "../pages/RevocationPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/Revocation",
  component: RevocationPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <RevocationPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Ihre Dateneingabe zur Stornierung",
    intro:
      "Wenn Sie Ihren Freischaltcode verloren haben oder aus anderen Gründen einen neuen beantragen wollen, können Sie den alten hier stornieren.",
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
      value: ["17", "11", "1954"],
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
    dob: {
      value: ["40", "11", "1954"],
      errors: ["Kein gültiges Datum"],
    },
  },
};
