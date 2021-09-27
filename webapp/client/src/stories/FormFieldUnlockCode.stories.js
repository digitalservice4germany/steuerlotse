import React from "react";

import FormFieldUnlockCode from "../components/FormFieldUnlockCode";
import StepForm from "../components/StepForm";
import * as StepFormStories from "./StepForm.stories";

export default {
  title: "Form Fields/Unlock Code",
  component: FormFieldUnlockCode,
};

const Template = (args) => (
  <StepForm {...StepFormStories.Default.args}>
    <FormFieldUnlockCode {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "unlock-code",
  fieldName: "unlock-code",
  label: {
    text: "Freischaltcode",
  },
  errors: [],
  values: [],
};
