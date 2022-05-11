import React from "react";
import SuccessStepsInfoBox from "../components/successStepsInfoBox";

export default {
  title: "Components/StepsInfoBox",
  component: SuccessStepsInfoBox,
};

function Template(args) {
  return <SuccessStepsInfoBox {...args} />;
}

export const Default = Template.bind({});
