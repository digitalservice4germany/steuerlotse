import React from "react";

import NoPauschbetragPage from "../pages/NoPauschbetragPage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/NoPauschbetrag",
  component: NoPauschbetragPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <NoPauschbetragPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title:
      "Leider haben Sie keinen Anspruch auf behinderungsbedingte Pauschbeträge.",
  },
  prevUrl: "/previous/step",
  nextUrl: "/next/step",
  showOverviewButton: false,
};
