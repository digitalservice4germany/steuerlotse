import React from "react";
import AmbassadorInfoMaterialPage from "../pages/AmbassadorInfoMaterialPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/AmbassadorInfoMaterialPage",
  component: AmbassadorInfoMaterialPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <AmbassadorInfoMaterialPage />;
}

export const Default = Template.bind({});
