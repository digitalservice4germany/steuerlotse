import React from "react";

import AnchorButton from "../components/AnchorButton";

export default {
  title: "Anchor Elements/Button",
  component: AnchorButton,
};

function Template(args) {
  return <AnchorButton {...args} />;
}

export const Default = Template.bind({});
export const DownloadLink = Template.bind({});

Default.args = {
  text: "Abmelden",
  url: "/download_preparation",
};

DownloadLink.args = {
  text: "Vorbereitungshilfe herunterladen",
  url: "/download_preparation",
  isDownloadLink: true,
};
