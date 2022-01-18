import React from "react";
import FahrtkostenpauschalePersonBPage from "../pages/FahrtkostenpauschalePersonBPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/FahrtkostenpauschalePersonBPage",
  component: FahrtkostenpauschalePersonBPage,
};

function Template(args) {
  return <FahrtkostenpauschalePersonBPage {...args} />;
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
    personBRequestsFahrtkostenpauschale: {
      errors: [],
    },
  },
  fahrtkostenpauschaleAmount: "1200",
  prevUrl: "fooUrl",
};
