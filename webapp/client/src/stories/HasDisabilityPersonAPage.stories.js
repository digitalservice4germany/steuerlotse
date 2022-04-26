import React from "react";

import HasDisabilityPersonAPage from "../pages/HasDisabilityPersonAPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/HasDisabilityPersonAPage",
  component: HasDisabilityPersonAPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <HasDisabilityPersonAPage {...args} />;
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
    personAHasDisability: {
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
    personAHasDisability: {
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
