import React from "react";

import TelephoneNumberPage from "../pages/TelephoneNumberPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/TelephoneNumber",
  component: TelephoneNumberPage,
};

function Template(args) {
  <TelephoneNumberPage {...args} />;
}

export const Default = Template.bind({});
export const WithValue = Template.bind({});
export const WithErrors = Template.bind({});

Default.args = {
  stepHeader: {
    title: "Telefonnummer für Rückfragen",
    intro:
      "Geben Sie eine Telefonnummer an, wenn Sie wünschen, dass Ihr Finanzamt Sie bei eventuellen Rückfragen kontaktieren kann.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    telephoneNumber: {
      value: "",
      errors: [],
    },
  },
  prevUrl: "/previous/step",
};

WithValue.args = {
  ...Default.args,
  fields: {
    telephoneNumber: {
      value: "555-2368-32168",
      errors: [],
    },
  },
};

WithErrors.args = {
  ...Default.args,
  fields: {
    telephoneNumber: {
      value: "25",
      errors: ["Die Angabe ist 5 Zeichen zu lang."],
    },
  },
};
