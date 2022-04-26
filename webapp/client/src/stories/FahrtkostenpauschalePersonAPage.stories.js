import React from "react";
import FahrtkostenpauschalePersonAPage from "../pages/FahrtkostenpauschalePersonAPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/FahrtkostenpauschalePersonAPage",
  component: FahrtkostenpauschalePersonAPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <FahrtkostenpauschalePersonAPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Behinderungsbedingte Fahrtkostenpauschale",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personARequestsFahrtkostenpauschale: {
      errors: [],
    },
  },
  fahrtkostenpauschaleAmount: "900",
  prevUrl: "fooUrl",
};
