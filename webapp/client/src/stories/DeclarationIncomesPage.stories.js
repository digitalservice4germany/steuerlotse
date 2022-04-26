import React from "react";

import DeclarationIncomesPage from "../pages/DeclarationIncomesPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/DeclarationIncomes",
  component: DeclarationIncomesPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <DeclarationIncomesPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Erklärung zu weiteren Einkünften",
    intro:
      "Sie können Ihre Steuererklärung nur mit diesem Service machen, wenn Sie und ggf. Ihr Partner bzw. Ihre Partnerin keine weiteren Einkünfte hatten, außer:",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    declarationIncomes: {
      errors: [],
    },
  },
};
