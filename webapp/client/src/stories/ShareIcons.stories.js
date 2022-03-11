import React from "react";
import ShareIcons from "../components/ShareIcons";

export default {
  title: "Anchor Elements/Share Icons",
  component: ShareIcons,
};

function Template(args) {
  return <ShareIcons {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  promoteUrl: "http://crossdivisions.com/",
  shareText:
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. ",
  mailSubject: "Get hypnotized and relax",
  sourcePage: "Bible",
};
