import React from "react";
import successStepsInfoBox from "../components/successStepsInfoBox";

export default {
  title: "Components/StepsInfoBox",
  component: successStepsInfoBox,
};

function Template(args) {
  return <successStepsInfoBox {...args} />;
}

export const Default = Template.bind({});
