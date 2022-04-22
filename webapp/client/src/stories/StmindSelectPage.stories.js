import React from "react";

import StmindSelectionPage from "../pages/StmindSelectionPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/StmindSelectionPage",
  component: StmindSelectionPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <StmindSelectionPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Ihre Ausgaben",
    intro:
      "Sie können eine Vielzahl an Ausgaben in Ihrer Steuererklärung angeben und somit Ihre Steuerbelastung reduzieren. Wählen Sie die Bereiche, in denen Sie Angaben machen möchten.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    stmindSelectVorsorge: {
      checked: false,
      errors: [],
    },
    stmindSelectAussergBela: {
      checked: false,
      errors: [],
    },
    stmindSelectHandwerker: {
      checked: false,
      errors: [],
    },
    stmindSelectSpenden: {
      checked: false,
      errors: [],
    },
    stmindSelectReligion: {
      checked: false,
      errors: [],
    },
  },
  prevUrl: "FooWebsite",
};
