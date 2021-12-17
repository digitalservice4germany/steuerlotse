import React from "react";

import PauschbetragPagePersonB from "../pages/PauschbetragPersonBPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/PauschbetragPersonB",
  component: PauschbetragPagePersonB,
};

function Template(args) {
  return <PauschbetragPagePersonB {...args} />;
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
