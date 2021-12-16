import React from "react";

import DisabilityQuestionPage from "../pages/DisabilityQuestionPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/DisabilityQuestionPage",
  component: DisabilityQuestionPage,
};

function Template(args) {
  return <DisabilityQuestionPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit machen?",
    intro:
      "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen in Anspruch nehmen.",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    disabilityExists: "Yes",
  },
  errors: [],
  prevUrl: "test",
};
