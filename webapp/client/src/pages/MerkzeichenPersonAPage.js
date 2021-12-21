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

export default function MerkzeichenPersonAPage({
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
          fieldName="person_a_has_pflegegrad"
          fieldId="person_a_has_pflegegrad"
          value={fields.personAHasPflegegrad.value}
          label={{
            text: t("lotse.merkzeichen.hasPflegegrad.label"),
          }}
          errors={fields.personAHasPflegegrad.errors}
        />
        <FormFieldIntegerInput
          fieldName="person_a_disability_degree"
          fieldId="person_a_disability_degree"
          value={fields.personADisabilityDegree.value}
          label={{
            text: t("lotse.merkzeichen.disabilityDegree.label"),
            exampleInput: t("lotse.merkzeichen.disabilityDegree.example"),
          }}
          fieldWidth={3}
          errors={fields.personADisabilityDegree.errors}
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
            fieldName="person_a_has_merkzeichen_g"
            fieldId="person_a_has_merkzeichen_g"
            checked={fields.personAHasMerkzeichenG.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenG.label")}
            errors={fields.personAHasMerkzeichenG.errors}
          />
          <FormFieldCheckBox
            fieldName="person_a_has_merkzeichen_ag"
            fieldId="person_a_has_merkzeichen_ag"
            checked={fields.personAHasMerkzeichenAg.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenAg.label")}
            errors={fields.personAHasMerkzeichenAg.errors}
          />
          <FormFieldCheckBox
            fieldName="person_a_has_merkzeichen_bl"
            fieldId="person_a_has_merkzeichen_bl"
            checked={fields.personAHasMerkzeichenBl.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenBl.label")}
            errors={fields.personAHasMerkzeichenBl.errors}
          />
          <FormFieldCheckBox
            fieldName="person_a_has_merkzeichen_tbl"
            fieldId="person_a_has_merkzeichen_tbl"
            checked={fields.personAHasMerkzeichenTbl.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenTbl.label")}
            errors={fields.personAHasMerkzeichenTbl.errors}
          />
          <FormFieldCheckBox
            fieldName="person_a_has_merkzeichen_h"
            fieldId="person_a_has_merkzeichen_h"
            checked={fields.personAHasMerkzeichenH.checked}
            labelText={t("lotse.merkzeichen.hasMerkzeichenH.label")}
            errors={fields.personAHasMerkzeichenH.errors}
          />
        </fieldset>
      </StepForm>
    </>
  );
}

MerkzeichenPersonAPage.propTypes = {
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
    personAHasPflegegrad: fieldPropType,
    personADisabilityDegree: fieldPropType,
    personAHasMerkzeichenH: checkboxPropType,
    personAHasMerkzeichenG: checkboxPropType,
    personAHasMerkzeichenBl: checkboxPropType,
    personAHasMerkzeichenTbl: checkboxPropType,
    personAHasMerkzeichenAg: checkboxPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
