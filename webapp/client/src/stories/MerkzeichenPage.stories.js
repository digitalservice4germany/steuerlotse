import React from "react";

import MerkzeichenPage from "../pages/MerkzeichenPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/Merkzeichen",
  component: MerkzeichenPage,
};

function Template(args) {
  return <MerkzeichenPage {...args} />;
}

export const Default = Template.bind({});
export const WithValue = Template.bind({});
export const WithErrors = Template.bind({});

Default.args = {
  stepHeader: {
    title: "Angaben zu Ihrer Behinderung oder Pflegebedürftigkeit",
    intro:
      "Bei einer Behinderung besteht in der Regel Anspruch auf steuerliche Vergünstigungen in Form von Pauschbeträgen. Ob und in welcher Höhe Sie Anspruch auf die Pauschbeträge haben, ist von Ihren Angaben abhängig.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    hasCareDegree: {
      value: "",
      errors: [],
    },
    disabilityDegree: {
      value: "",
      errors: [],
    },
    markH: {
      checked: false,
      errors: [],
    },
    markG: {
      checked: false,
      errors: [],
    },
    markBl: {
      checked: false,
      errors: [],
    },
    markTbl: {
      checked: false,
      errors: [],
    },
    markAg: {
      checked: false,
      errors: [],
    },
  },
  prevUrl: "/previous/step",
};
