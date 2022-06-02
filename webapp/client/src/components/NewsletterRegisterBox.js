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
  margin: 0 auto;
  padding: var(--spacing-05) var(--spacing-07a) var(--spacing-06a)
    var(--spacing-06a);

  @media (min-width: 769px) {
    padding: var(--spacing-07) var(--spacing-13) var(--spacing-07b)
      var(--spacing-07b);
  }
`;

const BoxHeadline = styled.h2`
  margin: 0;
  font-size: var(--text-medium-big);
  padding-bottom: var(--spacing-03);

  @media (min-width: 577px) {
    font-size: var(--text-xxl);
  }

  @media (min-width: 769px) {
    padding-bottom: var(--spacing-04a);
  }
`;
const BoxText = styled.span`
  font-size: var(--text-medium);
`;

const SmallText = styled.span`
  font-size: var(--text-medium);
  color: var(--secondary-text-color);
`;

const ButtonInRow = styled(ButtonAnchor)`
  margin-top: var(--spacing-05);
  @media (min-width: 577px) {
    margin-top: 47px;
  }
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

const RowFieldButton = styled.div`
  display: grid;
  @media (min-width: 577px) {
    display: flex;
  }
  flex-wrap: wrap;
  padding-bottom: var(--spacing-03);
`;

const ColumnField = styled.div`
  display: inline-block;

  @media (min-width: 577px) {
    flex-basis: ${({ flexBasis }) => `${flexBasis}%`};
  }

  ${({ reduceMargin }) =>
    reduceMargin &&
    `
      .text-input-field-label {
        margin-top: var(--spacing-05);
    }
  `}
`;

const ColumnButton = styled.div`
  display: inline-block;
  @media (min-width: 577px) {
    flex-basis: ${({ flexBasis }) => `${flexBasis}%`};
    ${({ leftAuto }) =>
      leftAuto &&
      `
    margin-left: auto;
  `}
  }
`;

const RowTickSuccessMessage = styled.div`
  display: flex;
  padding-bottom: var(--spacing-03);
`;

const ColumnTick = styled.div`
  display: inline-block;
  flex-basis: ${({ flexBasis }) => `${flexBasis}%`};
  margin-top: var(--spacing-03);
`;

const ColumnSuccessMessage = styled.div`
  display: inline-block;
  flex-basis: ${({ flexBasis }) => `${flexBasis}%`};
  margin-top: var(--spacing-03);
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
        <RowFieldButton>
          <ColumnField flexBasis={61.54} reduceMargin>
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
          </ColumnField>
          <ColumnButton flexBasis={30} leftAuto>
            <ButtonInRow onClick={sendEmail}>
              {t("newsletter.button.label")}
            </ButtonInRow>
          </ColumnButton>
        </RowFieldButton>
        <SuccessBox id="success">
          <RowTickSuccessMessage>
            <ColumnTick flexBasis={4.6}>
              <SuccessIconSmall />
            </ColumnTick>
            <ColumnSuccessMessage flexBasis={85.85}>
              <Trans
                t={t}
                i18nKey="newsletter.success.text"
                values={{ emailValue }}
              />
            </ColumnSuccessMessage>
          </RowTickSuccessMessage>
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
