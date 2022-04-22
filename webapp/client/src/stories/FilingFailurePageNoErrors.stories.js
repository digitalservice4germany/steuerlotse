import React from "react";
import FilingFailurePage from "../pages/FilingFailurePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/FilingFailurePageNoErrors",
  component: FilingFailurePage,
  decorators: baseDecorator,
};

export function Default() {
  return <FilingFailurePage />;
}
