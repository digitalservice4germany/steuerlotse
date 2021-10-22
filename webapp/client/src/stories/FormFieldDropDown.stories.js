import React from "react";

import FormFieldDropDown from "../components/FormFieldDropDown";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/DropDown",
  component: FormFieldDropDown,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldDropDown {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "dropDown",
  fieldName: "dropDown",
  label: {
    text: "Wen magst du am liebsten?",
  },
  errors: [],
  values: [
    ["han", "Han Solo"],
    ["luke", "Luke Skywalker"],
    ["rey", "Rey"],
    ["ben", "Obi-Wan Kenobi"],
  ],
};

export const DropDownWithDefaultValue = Template.bind({});
DropDownWithDefaultValue.args = {
  fieldId: "dropDown",
  fieldName: "dropDown",
  defaultValue: "Bitte auswählen",
  label: {
    text: "Wen magst du am liebsten?",
  },
  errors: [],
  values: [
    ["han", "Han Solo"],
    ["luke", "Luke Skywalker"],
    ["rey", "Rey"],
    ["ben", "Obi-Wan Kenobi"],
  ],
};
