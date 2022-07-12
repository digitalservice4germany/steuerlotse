import React from "react";
import HowItWorksComponent from "../components/HowItWorksComponent";
import OneIcon from "../assets/icons/Icon-1.svg";
import TwoIcon from "../assets/icons/Icon-2.svg";

export default {
  title: "Components/HowItWorksComponent",
  component: HowItWorksComponent,
  parameters: {
    layout: "centered",
  },
};

function Template(args) {
  return <HowItWorksComponent {...args} />;
}

export const NoText = Template.bind({});
NoText.args = {
  heading: "Vorbereiten und Belege sammeln",
  icon: {
    iconSrc: OneIcon,
  },
  image: {
    src: "../../images/step1.png",
    alt: "",
    srcSetDesktop: "../../images/step1.png",
    srcSetMobile: "../../images/step1_mobile.png",
  },
};

export const WithText = Template.bind({});
WithText.args = {
  heading: "Vorbereiten und Belege sammeln",
  text: "Wenn Sie die Steuererklärung gemeinsam als Paar machen möchten, reicht es aus, wenn sich eine Person registriert.",
  icon: {
    iconSrc: TwoIcon,
  },
  image: {
    src: "../../images/step1.png",
    alt: "",
    srcSetDesktop: "../../images/step1.png",
    srcSetMobile: "../../images/step1_mobile.png",
  },
};

export const NoSideBorder = Template.bind({});
NoSideBorder.args = {
  heading: "Vorbereiten und Belege sammeln",
  text: "Wenn Sie die Steuererklärung gemeinsam als Paar machen möchten, reicht es aus, wenn sich eine Person registriert.",
  icon: {
    iconSrc: TwoIcon,
  },
  variant: true,
  image: {
    src: "../../images/step1.png",
    alt: "",
    srcSetDesktop: "../../images/step1.png",
    srcSetMobile: "../../images/step1_mobile.png",
  },
};
