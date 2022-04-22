import React from "react";
import InfoBox from "../components/InfoBox";

export default {
  title: "Components/Info Box",
  component: InfoBox,
};

function Template(args) {
  return <InfoBox {...args} />;
}

export const Default = Template.bind({});
