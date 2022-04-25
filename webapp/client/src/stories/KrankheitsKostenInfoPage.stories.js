import React from "react";
import KrankheitsKostenInfoPage from "../pages/KrankheitsKostenInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/KrankheitskostenPage",
  component: KrankheitsKostenInfoPage,
  decorators: contentPageDecorator,
  layout: "padded",
  args: {
    fscRequestUrl: "/unlock_code_request/step/data_input?link_overview=False",
  },
};

function Template(args) {
  return <KrankheitsKostenInfoPage {...args} />;
}

export const Default = Template.bind({});
