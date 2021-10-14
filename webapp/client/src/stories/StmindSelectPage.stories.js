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
    stmind_select_vorsorge: {
      checked: false,
      errors: [],
    },
    stmind_select_ausserg_bela: {
      checked: false,
      errors: [],
    },
    stmind_select_handwerker: {
      checked: false,
      errors: [],
    },
    stmind_select_spenden: {
      checked: false,
      errors: [],
    },
    stmind_select_religion: {
      checked: false,
      errors: [],
    },
  },
};
