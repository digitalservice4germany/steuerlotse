import React from "react";

import FormFieldTextInput from "../components/FormFieldTextInput";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/TextInput",
  component: FormFieldTextInput,
};

function Template(args) {
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldTextInput {...args} />
    </StepForm>
  );
}

export const Default = Template.bind({});
export const WithValue = Template.bind({});
export const WithErrors = Template.bind({});
export const WithDetails = Template.bind({});
export const WithAllLabelExtras = Template.bind({});
export const WithFieldWidth = Template.bind({});
export const WithMaxLength = Template.bind({});
export const WithMaxLengthAndWidth = Template.bind({});

Default.args = {
  fieldId: "text-input",
  fieldName: "text-input",
  label: {
    text: "Text",
  },
  errors: [],
  value: "",
};

WithValue.args = {
  ...Default.args,
  value: "Dumbledore",
};

WithErrors.args = {
  ...Default.args,
  errors: ["Dieses Feld wird benötigt"],
};

WithDetails.args = {
  ...Default.args,
  details: {
    title: "Wann bekomme ich einen Freischaltcode?",
    text: "Sie bekommen einen Freischaltcode, wenn Sie sich bei Mein Elster mit einer Zertifikatsdatei identifiziert und keinen Abrufcode beantragt haben. Wenn Sie sich z.B. mit Ihrem Personalausweis, einer Karte oder einem Stick bei Mein Elster identifiziert oder einen Abrufcode beantragt haben, bekommen Sie den Brief mit dem Freischaltcode nicht.",
  },
};

WithAllLabelExtras.args = {
  ...WithDetails.args,
  label: {
    text: "Text",
    showOptionalTag: true,
    help: "Das ist ein Hilfetext. Hilft er dir?",
    exampleInput: "Beispiel",
  },
};

WithFieldWidth.args = {
  ...Default.args,
  fieldWidth: 4,
};

WithMaxLength.args = {
  ...Default.args,
  maxLength: 4,
};

WithMaxLengthAndWidth.args = {
  ...Default.args,
  maxLength: 4,
  fieldWidth: 4,
};
