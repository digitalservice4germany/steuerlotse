import React from "react";
import UnlockCodeSuccessPage from "../pages/UnlockCodeSuccessPage";

export default {
  title: "Pages/UnlockCodeSuccess",
  component: UnlockCodeSuccessPage,
};

function Template(args) {
  return <UnlockCodeSuccessPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Ihre Registrierung war erfolgreich!",
    intro:
      "Wir haben Ihren Antrag an Ihre Finanzverwaltung weitergeleitet. Sie können mit Ihrer Steuererklärung beginnen, " +
      "sobald Sie Ihren Freischaltcode erhalten haben. Es kann bis zu zwei Wochen dauern, bis Sie Ihren Brief erhalten.",
  },
  prevUrl: "/unlock_code_revocation/step/data_input",
  nextUrl: "/unlock_code_request/step/data_input",
  downloadUrl: "/download_preparation",
  download: true,
  steuerErklaerungsLink: "unlock_code_activation/step/data_input",
  vorbereitungshilfeLink: "/download_preparation",
};
