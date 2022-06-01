import React from "react";
import SuccessStepsInfoBox from "../components/SuccessStepsInfoBox";
import OneIcon from "../assets/icons/Icon-1.svg";

export default {
  title: "Components/StepsInfoBox",
  component: SuccessStepsInfoBox,
};

function Template(args) {
  return <SuccessStepsInfoBox {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  header: "Vorbereiten und Belege sammeln",
  text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben. Eine Übersicht über die notwendigen Unterlagen und Informationen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer Vorbereitungshilfe oder unter dem Menüpunkt Vorbereiten.",
  anchor: {
    url: "/download_preparation",
    text: "Vorbereitungshilfe speichern",
  },
  icon: {
    iconSrc: OneIcon,
  },
};
