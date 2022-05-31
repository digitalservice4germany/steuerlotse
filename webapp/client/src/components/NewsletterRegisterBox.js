import styled from "styled-components";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import PropTypes from "prop-types";
import ButtonAnchor from "./ButtonAnchor";
import FormFieldTextInput from "./FormFieldTextInput";
import { ReactComponent as SuccessIcon } from "../assets/icons/success_icon.svg";

const Box = styled.div`
  background-color: var(--beige-200);
  margin: 0 auto;
  max-width: var(--pages-max-width);
  margin-top: var(--spacing-03);
`;

const InnerBox = styled.div`
  padding: var(--spacing-07) var(--spacing-13) var(--spacing-07a)
    var(--spacing-07a);
  margin: 0 auto;
`;

const BoxHeadline = styled.h2`
  padding-bottom: var(--spacing-06);
  margin: 0;

  font-size: var(--text-xxl);
`;
const BoxText = styled.span`
  padding-bottom: var(--spacing-01);
`;

const SmallText = styled.span`
  font-size: var(--text-medium);
  color: var(--secondary-text-color);
`;

const ButtonInRow = styled(ButtonAnchor)`
  margin-top: 65px;
  width: 195px;
`;

const SuccessBox = styled.div`
  background-color: var(--white);
  display: none;
  margin-bottom: var(--spacing-03);
`;

const SuccessIconSmall = styled(SuccessIcon)`
  height: 30px;
  width: 30px;
  top: 16px;
  left: 24px;
  margin-left: var(--spacing-05);
  margin-right: var(--spacing-03);
`;

const Row = styled.div`
  display: flex;
  flex-wrap: wrap;
  padding-bottom: var(--spacing-03);
`;

const ColumnA = styled.div`
  display: inline-block;
  flex-basis: ${({ flexBasis }) => `${flexBasis}%`};
`;

const ColumnB = styled.div`
  display: inline-block;
  flex-basis: ${({ flexBasis }) => `${flexBasis}%`};
  ${({ leftAuto }) =>
    leftAuto &&
    `
    margin-left: auto;
  `}
`;

const errors = [];
let emailValue = "";

export default function NewsletterRegisterBox({ dataPrivacyLink, csrfToken }) {
  const { t } = useTranslation();

  function displaySuccessBox(activate) {
    const x = document.getElementById("success");
    if (activate) {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  const [, updateState] = React.useState();
  const forceUpdate = React.useCallback(() => {
    displaySuccessBox(false);
    updateState({});
  }, []);

  const sendEmail = () => {
    emailValue = document.getElementsByTagName("input")[0].value;
    if (emailValue === "") {
      errors.length = 0;
      errors.push(t("newsletter.errors.emailEmpty"));
      forceUpdate();
    } else {
      fetch("/register_user_with_doi", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ mail: emailValue }),
      })
        .then((r) =>
          r.json().then((data) => ({ status: r.status, body: data }))
        )
        .then((data) => {
          if (data.status === 200) {
            errors.length = 0;
            forceUpdate();
            displaySuccessBox(true);
          } else if (data.status === 400) {
            errors.length = 0;
            switch (data.body.code) {
              case "invalid_parameter":
                errors.push(t("newsletter.errors.emailInvalid"));
                break;
              case "duplicate_parameter":
                errors.push(t("newsletter.errors.emailDuplicate"));
                break;
              default:
            }
            forceUpdate();
          }
        });
    }
  };

  return (
    <Box>
      <InnerBox>
        <BoxHeadline>{t("newsletter.headline")}</BoxHeadline>
        <BoxText>{t("newsletter.text")}</BoxText>
        <Row>
          <ColumnA flexBasis={61.54}>
            <FormFieldTextInput
              fieldName="email"
              fieldId="email"
              value={emailValue}
              label={{
                text: t("newsletter.fieldEmail.label"),
              }}
              errors={errors}
              fieldWidth={11}
            />
          </ColumnA>
          <ColumnB flexBasis={30} leftAuto>
            <ButtonInRow onClick={sendEmail}>
              {t("newsletter.button.label")}
            </ButtonInRow>
          </ColumnB>
        </Row>
        <SuccessBox id="success">
          <Row>
            <ColumnA flexBasis={4.6}>
              <SuccessIconSmall />
            </ColumnA>
            <ColumnB flexBasis={85.85}>
              <Trans
                t={t}
                i18nKey="newsletter.success.text"
                values={{ emailValue }}
                components={{ underscore: <u /> }}
              />
            </ColumnB>
          </Row>
        </SuccessBox>
        <SmallText>
          <Trans
            t={t}
            i18nKey="newsletter.smallText"
            components={{
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              dataPrivacyLink: <a href={dataPrivacyLink} />,
            }}
          />
        </SmallText>
      </InnerBox>
    </Box>
  );
}

NewsletterRegisterBox.propTypes = {
  dataPrivacyLink: PropTypes.string.isRequired,
  csrfToken: PropTypes.string.isRequired,
};
