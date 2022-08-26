import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import { ReactComponent as ArrowUp } from "../assets/icons/arrow_up.svg";
import ButtonAnchor from "../components/ButtonAnchor";

const { Text, Icon } = ButtonAnchor;

const ButtonAnchorStyled = styled(ButtonAnchor)`
  font-size: var(--text-base);
  margin-right: var(--spacing-05);
`;

const Intro = styled.p`
  font-size: var(--text-medium);
  margin-top: var(--spacing-05);
  margin-bottom: var(--spacing-05);
`;

const LastSentence = styled.p`
  margin-top: var(--spacing-08);
`;

export default function NewHerePage() {
  const { t } = useTranslation();

  const trans = function translateText(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          retirementPageLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/ende" />
          ),
        }}
      />
    );
  };

  return (
    <>
      <div className="section-intro">
        <h1>{t("newHere.title")}</h1>
        <div>
          <Intro>{t("newHere.text1")}</Intro>
        </div>
      </div>

      <ButtonAnchorStyled url={t("newHere.url")}>
        <Text>{t("newHere.button")}</Text>
        <Icon hoverVariant="translate-x">
          <ArrowUp />
        </Icon>
      </ButtonAnchorStyled>
      <LastSentence>{trans("newHere.text2")}</LastSentence>
    </>
  );
}
