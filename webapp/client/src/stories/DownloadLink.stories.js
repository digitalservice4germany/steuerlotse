import React from "react";

import DownloadLink from "../components/DownloadLink";

export default {
  title: "Anchor Elements/Download",
  component: DownloadLink,
};

function Template(args) {
  return <DownloadLink {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  text: "Vorbereitungshilfe herunterladen",
  url: "/download_preparation",
};
