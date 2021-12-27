import React from "react";

import MerkzeichenPersonBPage from "../pages/MerkzeichenPersonBPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/MerkzeichenPersonB",
  component: MerkzeichenPersonBPage,
};

function Template(args) {
  return <MerkzeichenPersonBPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Angaben zu Behinderung oder Pflegebedürftigkeit von Person B",
    intro:
      "Bei einer Behinderung besteht in der Regel Anspruch auf steuerliche Vergünstigungen in Form von Pauschbeträgen. Ob und in welcher Höhe Sie Anspruch auf die Pauschbeträge haben, ist von Ihren Angaben abhängig.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personBHasPflegegrad: {
      value: "",
      errors: [],
    },
    personBDisabilityDegree: {
      value: "",
      errors: [],
    },
    personBHasMerkzeichenH: {
      checked: false,
      errors: [],
    },
    personBHasMerkzeichenG: {
      checked: false,
      errors: [],
    },
    personBHasMerkzeichenBl: {
      checked: false,
      errors: [],
    },
    personBHasMerkzeichenTbl: {
      checked: false,
      errors: [],
    },
    personBHasMerkzeichenAg: {
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
    personBHasPflegegrad: {
      value: "yes",
      errors: [],
    },
    personBDisabilityDegree: {
      value: "30",
      errors: [],
    },
    personBHasMerkzeichenH: {
      checked: true,
      errors: [],
    },
    personBHasMerkzeichenG: {
      checked: true,
      errors: [],
    },
    personBHasMerkzeichenBl: {
      checked: true,
      errors: [],
    },
    personBHasMerkzeichenTbl: {
      checked: true,
      errors: [],
    },
    personBHasMerkzeichenAg: {
      checked: true,
      errors: [],
    },
  },
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  fields: {
    personBHasPflegegrad: {
      value: "",
      errors: ["Wählen Sie eine Option aus um fortfahren zu können."],
    },
    personBDisabilityDegree: {
      value: "",
      errors: [
        "Sie haben einen Anspruch auf den Pauschbetrag erst ab einem Grad der Behinderung von 20. Lassen Sie das Feld leer, falls der Wert unter 20 liegt.",
      ],
    },
    personBHasMerkzeichenH: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personBHasMerkzeichenG: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personBHasMerkzeichenBl: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personBHasMerkzeichenTbl: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personBHasMerkzeichenAg: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
  },
};
