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
  body: "Beiträge zu bestimmten Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, sind Vorsorgeaufwendungen. Hierzu zählen Unfallversicherungen, Haftpflichtversicherungen und bestimmte Risikolebensversicherungen",
  title: "Vorsorgeaufwendungen",
  icon: vorsorgeIcon,
  errors: [],
  values: [],
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  errors: ["Sicher, dass Sie das nicht ankreuzen wollen?"],
};
