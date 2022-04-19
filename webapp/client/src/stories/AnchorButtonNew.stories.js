import React from "react";
import AnchorButtonNew from "../components/AnchorButtonNew";
import { ReactComponent as PlayIcon } from "../assets/icons/play_icon.svg";

const { Text, Icon } = AnchorButtonNew;

export default {
  title: "Anchor Elements/Anchor Button New",
  component: AnchorButtonNew,
};

function Template(args) {
  const text = "Abmelden";

  return (
    <AnchorButtonNew {...args}>
      <Text text={text} />
    </AnchorButtonNew>
  );
}

export const Primary = Template.bind({});
Primary.args = {
  url: "#",
};

function TemplateOutline(args) {
  const text = "Zur Übersicht";

  return (
    <AnchorButtonNew {...args}>
      <Text text={text} />
    </AnchorButtonNew>
  );
}

export const Outline = TemplateOutline.bind({});
Outline.args = {
  url: "#",
  variant: "outline",
};

function TemplateIcon(args) {
  const text = "Auf Youtube abspielen";

  return (
    <AnchorButtonNew {...args}>
      <Icon>
        <PlayIcon />
      </Icon>
      <Text text={text} />
    </AnchorButtonNew>
  );
}

export const WithIcon = TemplateIcon.bind({});
WithIcon.args = {
  url: "#",
};
