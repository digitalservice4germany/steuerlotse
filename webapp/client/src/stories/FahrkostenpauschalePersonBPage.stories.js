import React from "react";
import FahrkostenpauschalePersonBPage from "../pages/FahrkostenpauschalePersonBPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/FahrkostenpauschalePersonBPage",
  component: FahrkostenpauschalePersonBPage,
};

function Template(args) {
  return <FahrkostenpauschalePersonBPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Behinderungsbedingte Fahrtkostenpauschale für Person B",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personARequestsFahrkostenpauschale: {
      errors: [],
    },
  },
  fahrkostenpauschaleAmount: 1200,
  prevUrl: "fooUrl",
};
