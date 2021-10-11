import React from "react";

import FormFieldCard from "../components/FormFieldCard";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";
import vorsorgeIcon from "../assets/icons/vorsorge_icon.svg";

export default {
  title: "Form Fields/Card",
  component: FormFieldCard,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldCard {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "card",
  fieldName: "card",
  labelText:
    "Das ist eine Card. Sie kann ein Icon haben oder auch nicht. Außerdem kannst du gerne mal draufklicken.",
  labelTitle: "Titel der Card",
  icon: vorsorgeIcon,
  errors: [],
  values: [],
};
