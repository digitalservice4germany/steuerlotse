import React from "react";
import ButtonAnchor from "../components/ButtonAnchor";
import { ReactComponent as PlayIconInverse } from "../assets/icons/DefaultStatePlayIcon.svg";
import { ReactComponent as VectorRight } from "../assets/icons/vector.svg";

const { Text, Icon } = ButtonAnchor;

export default {
  title: "Anchor Elements/Button Anchor",
  component: ButtonAnchor,
  args: {
    url: "#",
    children: "Abmelden",
  },
};

function Template(args) {
  return <ButtonAnchor {...args} />;
}

export const Primary = Template.bind({});

export const Outline = Template.bind({});
Outline.args = {
  variant: "outline",
};

export const Download = Template.bind({});
Download.args = {
  ...Outline.args,
  download: true,
  children: "Download",
};

export const Narrow = Template.bind({});
Narrow.args = {
  buttonStyle: "narrow",
  children: "Facebook",
};

export const High = Template.bind({});
High.args = {
  buttonStyle: "high",
};

export const WithIcon = Template.bind({});
WithIcon.args = {
  children: (
    <Icon>
      <VectorRight />
    </Icon>
  ),
};

export const WithTextIconAndHoverEffect = Template.bind({});
WithTextIconAndHoverEffect.args = {
  children: (
    <>
      <Text>Weiter</Text>
      <Icon hoverVariant="translate-x">
        <VectorRight />
      </Icon>
    </>
  ),
};

export const OutlineHighWithIconLeft = Template.bind({});
OutlineHighWithIconLeft.args = {
  variant: "outline",
  ...High,
  children: (
    <>
      <Icon>
        <PlayIconInverse />
      </Icon>
      <Text>Auf Youtube abspielen</Text>
    </>
  ),
};
