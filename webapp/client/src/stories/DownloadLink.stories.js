import React from "react";
import DownloadLink from "../components/DownloadLink";

export default {
  title: "Anchor Elements/DownloadLink",
  component: DownloadLink,
};

function Template(args) {
  return <DownloadLink {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  text: "Übersicht speichern",
  url: "/download_pf/print.pdf",
};
