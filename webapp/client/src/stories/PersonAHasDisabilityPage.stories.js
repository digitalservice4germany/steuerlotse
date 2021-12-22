import React from "react";

import PersonAHasDisabilityPage from "../pages/PersonAHasDisabilityPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/PersonAHasDisabilityPage",
  component: PersonAHasDisabilityPage,
};

function Template(args) {
  return <PersonAHasDisabilityPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit machen?",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personA_hasDisability: {
      value: null,
    },
  },
  prevUrl: "test",
  numUsers: 1,
};

export const WithError = Template.bind({});
WithError.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit machen?",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personA_hasDisability: {
      value: "yes",
      errors: ["Falsche Eingabe"],
    },
  },
  prevUrl: "test",
  numUsers: 1,
};

export const JointTaxes = Template.bind({});
JointTaxes.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit machen zu Person A?",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personA_hasDisability: {
      value: "yes",
    },
  },
  prevUrl: "test",
  numUsers: 2,
};
