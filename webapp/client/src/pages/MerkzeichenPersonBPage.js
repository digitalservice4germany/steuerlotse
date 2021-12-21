import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { checkboxPropType, fieldPropType } from "../lib/propTypes";
import FormFieldYesNo from "../components/FormFieldYesNo";
import FormFieldIntegerInput from "../components/FormFieldIntegerInput";
import FormFieldCheckBox from "../components/FormFieldCheckBox";
import FieldLabelForSeparatedFields from "../components/FieldLabelForSeparatedFields";

export default function MerkzeichenPersonBPage({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormFieldYesNo
          fieldName="person_b_has_pflegegrad"
          fieldId="person_b_has_pflegegrad"
          value={fields.personBHasPflegegrad.value}
          label={{
            text: t("lotse.merkzeichen.hasPflegegrad.label"),
          }}
          errors={fields.personBHasPflegegrad.errors}
        />
        <FormFieldIntegerInput
          fieldName="person_b_disability_degree"
          fieldId="person_b_disability_degree"
          value={fields.personBDisabilityDegree.value}
          label={{
            text: t("lotse.merkzeichen.disabilityDegree.label"),
            exampleInput: t("lotse.merkzeichen.disabilityDegree.example"),
          }}
          fieldWidth={3}
          errors={fields.personBDisabilityDegree.errors}
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
            fieldName="person_b_has_merkzeichen_g"
            fieldId="person_b_has_merkzeichen_g"
            checked={fields.personBHasMerkzeichenG.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenG.label")}
            errors={fields.personBHasMerkzeichenG.errors}
          />
          <FormFieldCheckBox
            fieldName="person_b_has_merkzeichen_ag"
            fieldId="person_b_has_merkzeichen_ag"
            checked={fields.personBHasMerkzeichenAg.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenAg.label")}
            errors={fields.personBHasMerkzeichenAg.errors}
          />
          <FormFieldCheckBox
            fieldName="person_b_has_merkzeichen_bl"
            fieldId="person_b_has_merkzeichen_bl"
            checked={fields.personBHasMerkzeichenBl.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenBl.label")}
            errors={fields.personBHasMerkzeichenBl.errors}
          />
          <FormFieldCheckBox
            fieldName="person_b_has_merkzeichen_tbl"
            fieldId="person_b_has_merkzeichen_tbl"
            checked={fields.personBHasMerkzeichenTbl.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenTbl.label")}
            errors={fields.personBHasMerkzeichenTbl.errors}
          />
          <FormFieldCheckBox
            fieldName="person_b_has_merkzeichen_h"
            fieldId="person_b_has_merkzeichen_h"
            checked={fields.personBHasMerkzeichenH.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenH.label")}
            errors={fields.personBHasMerkzeichenH.errors}
          />
        </fieldset>
      </StepForm>
    </>
  );
}

MerkzeichenPersonBPage.propTypes = {
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
    personBHasPflegegrad: fieldPropType,
    personBDisabilityDegree: fieldPropType,
    personBHasMerkzeichenH: checkboxPropType,
    personBHasMerkzeichenG: checkboxPropType,
    personBHasMerkzeichenBl: checkboxPropType,
    personBHasMerkzeichenTbl: checkboxPropType,
    personBHasMerkzeichenAg: checkboxPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
