import React from "react";

import FormFieldConsentBox from "../components/FormFieldConsentBox";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/ConsentBox",
  component: FormFieldConsentBox,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldConsentBox {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "consentBox",
  fieldName: "consentBox",
  labelText:
    "Ich mag Consent Boxen. Wenn du sie auch magst, klicke doch mal hier drauf.",
  errors: [],
  values: [],
};
