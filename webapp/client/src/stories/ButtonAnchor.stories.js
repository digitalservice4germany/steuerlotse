import React from "react";
import ButtonAnchor from "../components/ButtonAnchor";
import { ReactComponent as PlayIconInverse } from "../assets/icons/DefaultStatePlayIcon.svg";
import { ReactComponent as VectorRight } from "../assets/icons/vector.svg";
import { baseDecorator } from "../../.storybook/decorators";

const { Text, Icon } = ButtonAnchor;

export default {
  title: "Anchor Elements/Button Anchor",
  component: ButtonAnchor,
  args: {
    children: <Text>Abmelden</Text>,
  },
  decorators: baseDecorator,
};

function Template(args) {
  return <ButtonAnchor {...args} />;
}

export const Primary = Template.bind({});

export const Outline = Template.bind({});
Outline.args = {
  variant: "outline",
};

export const Disabled = Template.bind({});
Disabled.args = {
  variant: "disabled",
};

export const Download = Template.bind({});
Download.args = {
  ...Outline.args,
  download: true,
  children: <Text>Download</Text>,
  url: "#",
};

export const Narrow = Template.bind({});
Narrow.args = {
  buttonStyle: "narrow",
  children: <Text>Facebook</Text>,
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

export const OutlineWithIconLeft = Template.bind({});
OutlineWithIconLeft.args = {
  variant: "outline",
  children: (
    <>
      <Icon>
        <PlayIconInverse />
      </Icon>
      <Text>Auf Youtube abspielen</Text>
    </>
  ),
};
