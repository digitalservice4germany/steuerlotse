import React from "react";

import SessionNotePage from "../pages/SessionNotePage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/SessionNote",
  component: SessionNotePage,
  decorators: baseDecorator,
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
