import React from "react";

import DisabilityQuestionPage from "../pages/DisabilityQuestionPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/DisabilityQuestionPage",
  component: DisabilityQuestionPage,
};

function Template(args) {
  return <DisabilityQuestionPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    disabilityExists: "Yes",
  },
  errors: [],
  prevUrl: "test",
};
