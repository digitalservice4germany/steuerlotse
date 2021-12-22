import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import {
  extendedCheckboxPropType,
  extendedFieldPropType,
} from "../lib/propTypes";
import FormFieldYesNo from "../components/FormFieldYesNo";
import FormFieldIntegerInput from "../components/FormFieldIntegerInput";
import FormFieldCheckBox from "../components/FormFieldCheckBox";
import FieldLabelForSeparatedFields from "../components/FieldLabelForSeparatedFields";

export default function MerkzeichenPage({ stepHeader, form, fields, prevUrl }) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormFieldYesNo
          fieldName={fields.hasPflegegrad.name}
          fieldId={fields.hasPflegegrad.name}
          value={fields.hasPflegegrad.value}
          label={{
            text: t("lotse.merkzeichen.hasPflegegrad.label"),
          }}
          errors={fields.hasPflegegrad.errors}
        />
        <FormFieldIntegerInput
          fieldName={fields.disabilityDegree.name}
          fieldId={fields.disabilityDegree.name}
          value={fields.disabilityDegree.value}
          label={{
            text: t("lotse.merkzeichen.disabilityDegree.label"),
            exampleInput: t("lotse.merkzeichen.disabilityDegree.example"),
          }}
          fieldWidth={3}
          errors={fields.disabilityDegree.errors}
        />
        <fieldset id="merkzeichen">
          <FieldLabelForSeparatedFields
            fieldId="merkzeichen"
            label={{ text: t("lotse.merkzeichen.merkzeichen.label") }}
            details={{
              title: t("lotse.merkzeichen.merkzeichen.details.title"),
              text: t("lotse.merkzeichen.merkzeichen.details.text"),
            }}
          />
          <FormFieldCheckBox
            fieldName={fields.hasMerkzeichenG.name}
            fieldId={fields.hasMerkzeichenG.name}
            checked={fields.hasMerkzeichenG.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenG.label")}
            errors={fields.hasMerkzeichenG.errors}
          />
          <FormFieldCheckBox
            fieldName={fields.hasMerkzeichenAg.name}
            fieldId={fields.hasMerkzeichenAg.name}
            checked={fields.hasMerkzeichenAg.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenAg.label")}
            errors={fields.hasMerkzeichenAg.errors}
          />
          <FormFieldCheckBox
            fieldName={fields.hasMerkzeichenBl.name}
            fieldId={fields.hasMerkzeichenBl.name}
            checked={fields.hasMerkzeichenBl.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenBl.label")}
            errors={fields.hasMerkzeichenBl.errors}
          />
          <FormFieldCheckBox
            fieldName={fields.hasMerkzeichenTbl.name}
            fieldId={fields.hasMerkzeichenTbl.name}
            checked={fields.hasMerkzeichenTbl.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenTbl.label")}
            errors={fields.hasMerkzeichenTbl.errors}
          />
          <FormFieldCheckBox
            fieldName={fields.hasMerkzeichenH.name}
            fieldId={fields.hasMerkzeichenH.name}
            checked={fields.hasMerkzeichenH.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenH.label")}
            errors={fields.hasMerkzeichenH.errors}
          />
        </fieldset>
      </StepForm>
    </>
  );
}

MerkzeichenPage.propTypes = {
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
    hasPflegegrad: extendedFieldPropType,
    disabilityDegree: extendedFieldPropType,
    hasMerkzeichenH: extendedCheckboxPropType,
    hasMerkzeichenG: extendedCheckboxPropType,
    hasMerkzeichenBl: extendedCheckboxPropType,
    hasMerkzeichenTbl: extendedCheckboxPropType,
    hasMerkzeichenAg: extendedCheckboxPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
