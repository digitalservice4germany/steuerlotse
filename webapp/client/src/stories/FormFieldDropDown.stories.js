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
  values: [
    ["bw", "Baden-Württemberg"],
    ["by", "Bayern"],
    ["hh", "Hamburg"],
    ["he", "Hessen"],
  ],
};

export const WithDetails = Template.bind({});
WithDetails.args = {
  fieldId: "dropDown",
  fieldName: "dropDown",
  label: {
    text: "Bundesland",
  },
  errors: [],
  details: {
    title: "Warum muss ich das auswählen?",
    text: "Die Finanzämter sind nach Bundesländern sortiert.",
  },
  values: [
    ["bw", "Baden-Württemberg"],
    ["by", "Bayern"],
    ["hh", "Hamburg"],
    ["he", "Hessen"],
  ],
};

export const PreSelection = Template.bind({});
PreSelection.args = {
  fieldId: "dropDown",
  fieldName: "dropDown",
  label: {
    text: "Bundesland",
  },
  errors: [],
  values: [
    ["bw", "Baden-Württemberg"],
    ["by", "Bayern"],
    ["hh", "Hamburg"],
    ["he", "Hessen"],
  ],
  preselectedValue: "by",
};

export const DefaultDropDownValue = Template.bind({});
DefaultDropDownValue.args = {
  fieldId: "dropDown",
  fieldName: "dropDown",
  defaultValue: "Bitte auswählen",
  label: {
    text: "Bundesland",
  },
  errors: [],
  values: [
    ["bw", "Baden-Württemberg"],
    ["by", "Bayern"],
    ["hh", "Hamburg"],
    ["he", "Hessen"],
  ],
};

export const WithChangeHandler = Template.bind({});
WithChangeHandler.args = {
  fieldId: "dropDown",
  fieldName: "dropDown",
  defaultValue: "Bitte auswählen",
  label: {
    text: "Bundesland",
  },
  errors: [],
  values: [
    ["bw", "Baden-Württemberg"],
    ["by", "Bayern"],
    ["hh", "Hamburg"],
    ["he", "Hessen"],
  ],
  onChangeHandler: (event) => {
    alert(`Sie leben in ${event.target.selectedOptions[0].text}.`);
  },
};
