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

export const WithValues = Template.bind({});
WithValues.args = {
  ...Default.args,
  fields: {
    hasCareDegree: {
      value: "yes",
      errors: [],
    },
    disabilityDegree: {
      value: "30",
      errors: [],
    },
    markH: {
      checked: true,
      errors: [],
    },
    markG: {
      checked: true,
      errors: [],
    },
    markBl: {
      checked: true,
      errors: [],
    },
    markTbl: {
      checked: true,
      errors: [],
    },
    markAg: {
      checked: true,
      errors: [],
    },
  },
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  fields: {
    hasCareDegree: {
      value: "",
      errors: ["Wählen Sie eine Option aus um fortfahren zu können."],
    },
    disabilityDegree: {
      value: "",
      errors: [
        "Sie haben einen Anspruch auf den Pauschbetrag erst ab einem Grad der Behinderung von 20. Lassen Sie das Feld leer, falls der Wert unter 20 liegt.",
      ],
    },
    markH: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    markG: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    markBl: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    markTbl: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    markAg: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
  },
};
