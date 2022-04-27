import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import CraftsmanServicesInfoPage from "../pages/CraftsmanServicesInfoPage";

export default {
  title: "Content Pages/CraftsmanServicesInfoPage",
  component: CraftsmanServicesInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <CraftsmanServicesInfoPage />;
}

export const Default = Template.bind({});
