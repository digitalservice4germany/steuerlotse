import React from "react";
import { withDesign } from "storybook-addon-designs";
import ButtonAnchor from "../components/ButtonAnchor";
import { ReactComponent as PlayIconInverse } from "../assets/icons/DefaultStatePlayIcon.svg";
import { ReactComponent as VectorRight } from "../assets/icons/vector.svg";

const { Text, Icon } = ButtonAnchor;

export default {
  title: "Anchor Elements/Button Anchor",
  component: ButtonAnchor,
  decorators: [withDesign],
  args: {
    children: <Text>Abmelden</Text>,
  },
};

function Template(args) {
  return <ButtonAnchor {...args} />;
}

export const Primary = Template.bind({});
Primary.parameters = {
  design: {
    type: "figma",
    url: "https://www.figma.com/file/3BFAwyOiqaAul9lsO61Nfp/Steuerlotse-Draft-%26-Handover?node-id=3463%3A38237",
  },
};

export const Outline = Template.bind({});
Outline.args = {
  variant: "outline",
};

export const Disabled = Template.bind({});
Disabled.args = {
  disabled: true,
};

export const OutlineDisabled = Template.bind({});
OutlineDisabled.args = {
  ...Outline.args,
  ...Disabled.args,
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

export const WithIconHoverEffect = Template.bind({});
WithIconHoverEffect.args = {
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
