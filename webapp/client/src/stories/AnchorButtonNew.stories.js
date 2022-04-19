import React from "react";
import AnchorButtonNew from "../components/AnchorButtonNew";

export default {
  title: "Anchor Elements/Anchor Button New",
  component: AnchorButtonNew,
};

function Template(args) {
  return <AnchorButtonNew {...args} />;
}

export const Primary = Template.bind({});
Primary.args = {
  children: "Abmelden",
  url: "#",
};
