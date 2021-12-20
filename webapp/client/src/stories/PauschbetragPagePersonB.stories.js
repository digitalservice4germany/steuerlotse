import React from "react";

import PauschbetragPersonBPage from "../pages/PauschbetragPersonBPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/PauschbetragPersonB",
  component: PauschbetragPersonBPage,
};

function Template(args) {
  return <PauschbetragPersonBPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Pauschbetrag für Menschen mit Behinderung",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personBWantsPauschbetrag: {
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

export const WithValue = Template.bind({});
WithValue.args = {
  ...Default.args,
  fields: {
    personBWantsPauschbetrag: {
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

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  fields: {
    personBWantsPauschbetrag: {
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
