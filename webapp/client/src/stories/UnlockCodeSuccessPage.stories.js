import React from "react";
import UnlockCodeSuccessPage from "../pages/UnlockCodeSuccessPage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/UnlockCodeSuccess",
  component: UnlockCodeSuccessPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <UnlockCodeSuccessPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/unlock_code_revocation/step/data_input",
  vorbereitungsHilfeLink: "/download_preparation",
  dataPrivacyLink: "/datenschutz",
};
