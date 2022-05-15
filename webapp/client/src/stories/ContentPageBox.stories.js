import React from "react";
import ContentPageBox from "../components/ContentPageBox";

export default {
  title: "Components/Secondary ContentPageInfoBox",
  component: ContentPageBox,
};

function Template(args) {
  return <ContentPageBox {...args} />;
}

export const Default = Template.bind({});
