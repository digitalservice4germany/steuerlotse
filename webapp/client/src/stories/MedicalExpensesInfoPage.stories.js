import React from "react";
import MedicalExpensesInfoPage from "../pages/MedicalExpensesInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/MedicalExpensesInfoPage",
  component: MedicalExpensesInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <MedicalExpensesInfoPage />;
}

export const Default = Template.bind({});
