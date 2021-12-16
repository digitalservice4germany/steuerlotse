import React from "react";

import HasDisabilityPage from "../pages/HasDisabilityPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/HasDisabilityPage",
  component: HasDisabilityPage,
};

function Template(args) {
  return <HasDisabilityPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    hasDisability: "Yes",
  },
  errors: [],
  prevUrl: "test",
};
