import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import HouseholdServicesInfoPage from "../pages/HouseholdServicesInfoPage";

export default {
  title: "Content Pages/HouseholdServicesInfoPage",
  component: HouseholdServicesInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <HouseholdServicesInfoPage />;
}

export const Default = Template.bind({});
