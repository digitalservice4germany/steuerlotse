import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import DonationInfoPage from "../pages/DonationInfoPage";

export default {
  title: "Content Pages/DonationInfoPage",
  component: DonationInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <DonationInfoPage />;
}

export const Default = Template.bind({});
