import React from "react";

import SessionNotePage from "../pages/SessionNotePage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/SessionNote",
  component: SessionNotePage,
};

function Template(args) {
  return <SessionNotePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  form: {
    ...StepFormDefault,
    showOverviewButton: true,
  },
  prevUrl: "/previous/step",
};
