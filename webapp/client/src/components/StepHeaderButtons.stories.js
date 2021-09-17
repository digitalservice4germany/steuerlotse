import React from "react";

import StepHeaderButtons from "./StepHeaderButtons";

export default {
  title: "Forms/Step Header Buttons",
  component: StepHeaderButtons,
  decorators: [
    (
      Story // Render context from app/templates/basis/base.html
    ) => (
      <div className="main-content">
        <div className="mt-4">
          <div className="col-lg-9 col-md-10 col-xs-12 p-0">
            <Story />
          </div>
        </div>
      </div>
    ),
  ],
};

const Template = (args) => <StepHeaderButtons {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  backLinkUrl: "#something",
  backLinkText: "Zurück",
};
