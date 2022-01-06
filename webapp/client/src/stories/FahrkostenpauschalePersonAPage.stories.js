import React from "react";
import FahrkostenpauschalePersonAPage from "../pages/FahrkostenpauschalePersonAPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/FahrkostenpauschalePersonAPage",
  component: FahrkostenpauschalePersonAPage,
};

function Template(args) {
  return <FahrkostenpauschalePersonAPage {...args} />;
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
    personARequestsFahrkostenpauschale: {
      errors: [],
    },
  },
  fahrkostenpauschaleAmount: "900",
  prevUrl: "fooUrl",
};
