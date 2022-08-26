import React from "react";

import NewHere from "../pages/NewHerePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/NewHere",
  component: NewHere,
  decorators: baseDecorator,
};

function Template(args) {
  return <NewHere {...args} />;
}

export const Default = Template.bind({});
