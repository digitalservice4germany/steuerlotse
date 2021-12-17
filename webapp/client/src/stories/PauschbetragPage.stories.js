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
    intro:
      "Auf Basis Ihrer Angaben haben Sie Anspruch auf den Pauschbetrag für Menschen mit Behinderung.  Alternativ können die tatsächlichen Kosten, die in Zusammenhang mit Ihrer Behinderung entstanden sind, einzeln angegeben werden. Wählen Sie aus, ob Sie den Pauschbetrag in Anspruch nehmen möchten.",
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
          displayName: "Pauschbetrag in Höhe von <b>860</b> Euro beantragen",
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
