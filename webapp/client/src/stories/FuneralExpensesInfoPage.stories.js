import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import FuneralExpensesInfoPage from "../pages/FuneralExpensesInfoPage";

export default {
  title: "Content Pages/FuneralExpensesInfoPage",
  component: FuneralExpensesInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <FuneralExpensesInfoPage />;
}

export const Default = Template.bind({});
