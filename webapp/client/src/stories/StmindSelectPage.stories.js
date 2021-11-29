import React from "react";

import StmindSelectionPage from "../pages/StmindSelectionPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/StmindSelectionPage",
  component: StmindSelectionPage,
};

const Template = (args) => <StmindSelectionPage {...args} />;

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Ihre Ausgaben",
    intro:
      "Sie können eine Vielzahl an Ausgaben in Ihrer Steuererklärung angeben und somit Ihre Steuerlast reduzieren. Wählen Sie die Bereiche aus, in denen Sie im Besteuerungsjahr Ausgaben hatten.",
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
