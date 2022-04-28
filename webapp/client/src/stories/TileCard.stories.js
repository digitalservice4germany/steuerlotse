import React from "react";
import TileCard from "../components/TileCard";
import vorsorgeaufwendungenIcon from "../assets/icons/vorsorgeaufwendungen.svg";

export default {
  title: "Form Field/Tile Card",
  component: TileCard,
};

function Template(args) {
  return <TileCard {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  title: "Vorsorgeaufwendungen",
  icon: vorsorgeaufwendungenIcon,
  url: "to/url",
};
