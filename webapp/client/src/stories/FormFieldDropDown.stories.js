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
    text: "Bundesland",
  },
  errors: [],
  options: [
    { value: "bw", displayName: "Baden-Württemberg" },
    { value: "by", displayName: "Bayern" },
    { value: "hh", displayName: "Hamburg" },
    { value: "he", displayName: "Hessen" },
  ],
};

export const WithDetails = Template.bind({});
WithDetails.args = {
  ...Default.args,
  details: {
    title: "Warum muss ich das auswählen?",
    text: "Die Finanzämter sind nach Bundesländern sortiert.",
  },
};

export const PreSelection = Template.bind({});
PreSelection.args = {
  ...Default.args,
  selectedValue: "by",
};

export const DefaultDropDownOption = Template.bind({});
DefaultDropDownOption.args = {
  ...Default.args,
  defaultOption: "Bitte auswählen",
};

export const WithChangeHandler = Template.bind({});
WithChangeHandler.args = {
  ...Default.args,
  onChangeHandler: (event) => {
    alert(`Sie leben in ${event.target.selectedOptions[0].text}.`);
  },
};
