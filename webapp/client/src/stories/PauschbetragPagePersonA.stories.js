import React from "react";

import PauschbetragPagePersonA from "../pages/PauschbetragPersonAPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/PauschbetragPersonA",
  component: PauschbetragPagePersonA,
};

function Template(args) {
  return <PauschbetragPagePersonA {...args} />;
}

export const Default = Template.bind({});
export const WithValue = Template.bind({});
export const WithErrors = Template.bind({});

Default.args = {
  stepHeader: {
    title: "Pauschbetrag für Menschen mit Behinderung",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personAWantsPauschbetrag: {
      selectedValue: undefined,
      options: [
        {
          value: "yes",
          displayName:
            "Pauschbetrag in Höhe von <bold>860</bold> Euro beantragen",
        },
        {
          value: "no",
          displayName:
            "Kosten einzeln angeben und Pauschbetrag nicht beantragen",
        },
      ],
      errors: [],
    },
  },
  prevUrl: "/previous/step",
};

WithValue.args = {
  ...Default.args,
  fields: {
    personAWantsPauschbetrag: {
      selectedValue: "yes",
      options: [
        {
          value: "yes",
          displayName:
            "Pauschbetrag in Höhe von <bold>860</bold> Euro beantragen",
        },
        {
          value: "no",
          displayName:
            "Kosten einzeln angeben und Pauschbetrag nicht beantragen",
        },
      ],
      errors: [],
    },
  },
};

WithErrors.args = {
  ...Default.args,
  fields: {
    personAWantsPauschbetrag: {
      selectedValue: undefined,
      options: [
        {
          value: "yes",
          displayName:
            "Pauschbetrag in Höhe von <bold>860</bold> Euro beantragen",
        },
        {
          value: "no",
          displayName:
            "Kosten einzeln angeben und Pauschbetrag nicht beantragen",
        },
      ],
      errors: ["Bitte füllen Sie dieses Feld aus um weiterzumachen."],
    },
  },
};
