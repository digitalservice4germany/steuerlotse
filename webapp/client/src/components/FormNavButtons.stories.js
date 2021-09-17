import React from "react";
import FormNavButtons from "./FormNavButtons";

export default {
  title: "Forms/Nav Buttons",
  component: FormNavButtons,
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

const Template = (args) => <FormNavButtons {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  nextButtonLabel: "Weiter",
};

export const WithOverviewLink = Template.bind({});
WithOverviewLink.args = {
  ...Primary.args,
  overviewButton: true,
};

export const WithExplanatoryText = Template.bind({});
WithExplanatoryText.args = {
  ...Primary.args,
  explanatoryButtonText:
    'Sie haben Ihren Freischaltcode bereits erhalten? <br><a href="#">Dann können Sie sich anmelden</a>',
};
