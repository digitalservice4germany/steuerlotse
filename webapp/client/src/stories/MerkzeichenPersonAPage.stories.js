import React from "react";

import MerkzeichenPersonAPage from "../pages/MerkzeichenPersonAPage";
import { Default as StepFormDefault } from "./StepForm.stories";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/MerkzeichenPersonA",
  component: MerkzeichenPersonAPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <MerkzeichenPersonAPage {...args} />;
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
    personAHasPflegegrad: {
      value: "",
      errors: [],
    },
    personADisabilityDegree: {
      value: "",
      errors: [],
    },
    personAHasMerkzeichenH: {
      checked: false,
      errors: [],
    },
    personAHasMerkzeichenG: {
      checked: false,
      errors: [],
    },
    personAHasMerkzeichenBl: {
      checked: false,
      errors: [],
    },
    personAHasMerkzeichenTbl: {
      checked: false,
      errors: [],
    },
    personAHasMerkzeichenAg: {
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
    personAHasPflegegrad: {
      value: "yes",
      errors: [],
    },
    personADisabilityDegree: {
      value: "30",
      errors: [],
    },
    personAHasMerkzeichenH: {
      checked: true,
      errors: [],
    },
    personAHasMerkzeichenG: {
      checked: true,
      errors: [],
    },
    personAHasMerkzeichenBl: {
      checked: true,
      errors: [],
    },
    personAHasMerkzeichenTbl: {
      checked: true,
      errors: [],
    },
    personAHasMerkzeichenAg: {
      checked: true,
      errors: [],
    },
  },
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  fields: {
    personAHasPflegegrad: {
      value: "",
      errors: ["Wählen Sie eine Option aus um fortfahren zu können."],
    },
    personADisabilityDegree: {
      value: "",
      errors: [
        "Sie haben einen Anspruch auf den Pauschbetrag erst ab einem Grad der Behinderung von 20. Lassen Sie das Feld leer, falls der Wert unter 20 liegt.",
      ],
    },
    personAHasMerkzeichenH: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personAHasMerkzeichenG: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personAHasMerkzeichenBl: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personAHasMerkzeichenTbl: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
    personAHasMerkzeichenAg: {
      checked: false,
      errors: ["Ungültige Auswahl"],
    },
  },
};
