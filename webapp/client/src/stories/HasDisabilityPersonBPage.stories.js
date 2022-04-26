import React from "react";

import HasDisabilityPersonBPage from "../pages/HasDisabilityPersonBPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/HasDisabilityPersonBPage",
  component: HasDisabilityPersonBPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <HasDisabilityPersonBPage {...args} />;
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
    personBHasDisability: {
      value: null,
      errors: [],
    },
  },
  prevUrl: "test",
  numUsers: 1,
};

export const WithError = Template.bind({});
WithError.args = {
  ...Default.args,
  fields: {
    personBHasDisability: {
      value: "yes",
      errors: ["Falsche Eingabe"],
    },
  },
};

export const JointTaxes = Template.bind({});
JointTaxes.args = {
  ...Default.args,
  numUsers: 2,
};
