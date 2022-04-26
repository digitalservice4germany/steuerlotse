import React from "react";

import SecondaryAnchorButton from "../components/SecondaryAnchorButton";

export default {
  title: "Anchor Elements/Secondary Button -deprecated-",
  component: SecondaryAnchorButton,
};

function Template(args) {
  return <SecondaryAnchorButton {...args} />;
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
