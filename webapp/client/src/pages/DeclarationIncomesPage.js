import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import listMarker from "../assets/icons/list_marker.svg";
import { checkboxPropType } from "../lib/propTypes";

const IntroList = styled.ul`
  margin-bottom: var(--spacing-06);

  &.form-list {
    list-style-image: url(${listMarker});
  }

  &.form-list li::before {
    vertical-align: text-top;
    height: 1px;
  }

  &.form-list li {
    margin-top: var(--spacing-02);
  }
`;

export default function DeclarationIncomesPage({ stepHeader, form, fields }) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <IntroList className="form-list">
        <li>{t("lotse.declarationIncomes.listItem1")}</li>
        <li>{t("lotse.declarationIncomes.listItem2")}</li>
        <li>{t("lotse.declarationIncomes.listItem3")}</li>
      </IntroList>
      <StepForm {...form}>
        <FormFieldConsentBox
          autofocus
          required
          fieldName="declaration_incomes"
          fieldId="declaration_incomes"
          checked={fields.declarationIncomes.checked}
          labelText={t("lotse.fieldDeclarationIncomes.fieldConfirmIncomes")}
          errors={fields.declarationIncomes.errors}
        />
      </StepForm>
    </>
  );
}

DeclarationIncomesPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    declarationIncomes: checkboxPropType,
  }).isRequired,
};
