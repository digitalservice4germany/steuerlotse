import React from "react";

import NoPauschbetragPage from "../pages/NoPauschbetragPage";

export default {
  title: "Pages/NoPauschbetrag",
  component: NoPauschbetragPage,
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
