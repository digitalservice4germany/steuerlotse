import React from "react";
import PensionExpensesInfoPage from "../pages/PensionExpensesInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/PensionExpensesInfoPage",
  component: PensionExpensesInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <PensionExpensesInfoPage />;
}

export const Default = Template.bind({});
