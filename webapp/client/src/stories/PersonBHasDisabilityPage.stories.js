import React from "react";

import PersonBHasDisabilityPage from "../pages/PersonBHasDisabilityPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/PersonBHasDisabilityPage",
  component: PersonBHasDisabilityPage,
};

function Template(args) {
  return <PersonBHasDisabilityPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit für Person B machen?",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personBHasDisability: {
      value: null,
    },
  },
  prevUrl: "test",
};

export const WithError = Template.bind({});
WithError.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit für Person B machen?",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personBHasDisability: {
      value: "yes",
      errors: ["Falsche Eingabe"],
    },
  },
  prevUrl: "test",
};
