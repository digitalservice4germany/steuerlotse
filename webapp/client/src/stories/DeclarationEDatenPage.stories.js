import React from "react";

import DeclarationEDatenPage from "../pages/DeclarationEDatenPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/DeclarationEDatenPage",
  component: DeclarationEDatenPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <DeclarationEDatenPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Einverständnis zur automatischen Übernahme vorliegender Daten",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    declarationEdaten: {
      checked: false,
      errors: [],
    },
  },
  prevUrl: "/some/prev/path",
};
