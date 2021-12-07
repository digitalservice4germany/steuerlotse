import React from "react";

import ConfirmationPage from "../pages/ConfirmationPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/Confirmation",
  component: ConfirmationPage,
};

function Template(args) {
  return <ConfirmationPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Bestätigung und Versand an Ihre Finanzverwaltung",
    intro:
      "Diese Erklärung ist eine Einkommensteuererklärung im Sinne des § 150 Abs. 1 der Abgabenordnung (AO) i. V. m. § 25 des Einkommensteuergesetzes (EStG). Die mit der Erklärung angeforderten Daten werden aufgrund der §§ 149 und 150 AO und der §§ 25 und 46 EStG erhoben.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    confirmDataPrivacy: {
      errors: [],
    },
    confirmTermsOfService: {
      errors: [],
    },
  },
  termsOfServiceLink: "/agb",
  dataPrivacyLink: "/datenschutz",
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  fields: {
    confirmDataPrivacy: {
      errors: [
        "Bestätigen Sie, dass Sie mit der Datenschutzrichtlinien einverstanden sind, um fortfahren zu können.",
      ],
    },
    confirmTermsOfService: {
      errors: [
        "Bestätigen Sie, dass Sie den Nutzungbedingungen zustimmen,  um fortfahren zu können.",
      ],
    },
  },
};
