import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { checkboxPropType, fieldPropType } from "../lib/propTypes";
import FormFieldYesNo from "../components/FormFieldYesNo";
import FormFieldTextInput from "../components/FormFieldTextInput";
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
          fieldName="has_care_degree"
          fieldId="has_care_degree"
          value={fields.hasCareDegree.value}
          label={{
            text: t("lotse.merkzeichen.hasCareDegree.label"),
          }}
          errors={fields.hasCareDegree.errors}
        />
        <FormFieldTextInput
          fieldName="disability_degree"
          fieldId="disability_degree"
          value={fields.disabilityDegree.value}
          label={{
            text: t("lotse.merkzeichen.disabilityDegree.label"),
            exampleInput: t("lotse.merkzeichen.disabilityDegree.example"),
          }}
          maxWidth={3}
          errors={fields.disabilityDegree.errors}
        />
        <fieldset id="marks">
          <FieldLabelForSeparatedFields
            fieldId="marks"
            label={{ text: t("lotse.merkzeichen.marks.label") }}
            details={{
              title: t("lotse.merkzeichen.marks.details.title"),
              text: t("lotse.merkzeichen.marks.details.text"),
            }}
          />
          <FormFieldCheckBox
            fieldName="mark_g"
            fieldId="mark_g"
            checked={fields.markG.checked}
            labelText={t("lotse.merkzeichen.markG.label")}
            errors={fields.markG.errors}
          />
          <FormFieldCheckBox
            fieldName="mark_ag"
            fieldId="mark_ag"
            checked={fields.markAg.checked}
            labelText={t("lotse.merkzeichen.markAg.label")}
            errors={fields.markAg.errors}
          />
          <FormFieldCheckBox
            fieldName="mark_bl"
            fieldId="mark_bl"
            checked={fields.markBl.checked}
            labelText={t("lotse.merkzeichen.markBl.label")}
            errors={fields.markBl.errors}
          />
          <FormFieldCheckBox
            fieldName="mark_tbl"
            fieldId="mark_tbl"
            checked={fields.markTbl.checked}
            labelText={t("lotse.merkzeichen.markTbl.label")}
            errors={fields.markTbl.errors}
          />
          <FormFieldCheckBox
            fieldName="mark_h"
            fieldId="mark_h"
            checked={fields.markH.checked}
            labelText={t("lotse.merkzeichen.markH.label")}
            errors={fields.markH.errors}
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
    hasCareDegree: fieldPropType,
    disabilityDegree: fieldPropType,
    markH: checkboxPropType,
    markG: checkboxPropType,
    markBl: checkboxPropType,
    markTbl: checkboxPropType,
    markAg: checkboxPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
