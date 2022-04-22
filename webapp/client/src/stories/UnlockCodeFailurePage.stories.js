import React from "react";
import UnlockCodeFailurePage from "../pages/UnlockCodeFailurePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/UnlockCodeFailurePage",
  component: UnlockCodeFailurePage,
  decorators: baseDecorator,
};

function Template(args) {
  return <UnlockCodeFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/unlock_code_revocation/step/data_input",
};
