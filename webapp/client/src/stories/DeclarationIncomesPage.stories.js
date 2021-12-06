import React from "react";

import DeclarationIncomesPage from "../pages/DeclarationIncomesPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/DeclarationIncomes",
  component: DeclarationIncomesPage,
};

function Template(args) {
  <DeclarationIncomesPage {...args} />;
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
