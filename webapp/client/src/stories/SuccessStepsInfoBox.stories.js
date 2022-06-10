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

export const OnlyText = Template.bind({});
OnlyText.args = {
  header: "Vorbereiten und Belege sammeln",
  text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben. Eine Übersicht über die notwendigen Unterlagen und Informationen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer Vorbereitungshilfe oder unter dem Menüpunkt Vorbereiten.",
  textOnly: true,
};

export const NoIcon = Template.bind({});
NoIcon.args = {
  header: "Vorbereiten und Belege sammeln",
  text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben. Eine Übersicht über die notwendigen Unterlagen und Informationen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer Vorbereitungshilfe oder unter dem Menüpunkt Vorbereiten.",
  anchor: {
    url: "/download_preparation",
    text: "Vorbereitungshilfe speichern",
  },
};

export const WithImage = Template.bind({});
WithImage.args = {
  header: "Vorbereiten und Belege sammeln",
  text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben. Eine Übersicht über die notwendigen Unterlagen und Informationen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer Vorbereitungshilfe oder unter dem Menüpunkt Vorbereiten.",
  image: {
    src: "../../images/Img_Brief_500.jpg",
    alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
    srcSet:
      "../../images/Img_Brief_500.jpg 1155w ,  ../../images/Img_Brief_1024.jpg 2048w",
  },
  icon: {
    iconSrc: OneIcon,
  },
};

export const ContentShareBox = Template.bind({});
ContentShareBox.args = {
  header: "Artikel teilen",
  text: "Dieser Artikel kann auch hilfreich für Ihre Freunde und Bekannte sein?",
  shareText: "share text",
  mailSubject: "Mail Subject",
  sourcePage: "Reference Page",
  shareBoxSpacingVariant: true,
};
