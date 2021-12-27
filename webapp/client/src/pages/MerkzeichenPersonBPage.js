import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import { checkboxPropType, fieldPropType } from "../lib/propTypes";
import MerkzeichenPage from "./MerkzeichenPage";

export default function MerkzeichenPersonBPage({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  const { t } = useTranslation();

  return (
    <MerkzeichenPage
      {...{ stepHeader, form, prevUrl }}
      fields={{
        hasPflegegrad: {
          ...fields.personBHasPflegegrad,
          name: "person_b_has_pflegegrad",
          label: {
            text: t("lotse.merkzeichen.hasPflegegrad.label"),
          },
        },
        disabilityDegree: {
          ...fields.personBDisabilityDegree,
          name: "person_b_disability_degree",
          label: {
            text: t("lotse.merkzeichen.disabilityDegree.label"),
            exampleInput: t("lotse.merkzeichen.disabilityDegree.example"),
          },
        },
        hasMerkzeichenG: {
          ...fields.personBHasMerkzeichenG,
          name: "person_b_has_merkzeichen_g",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenG.label"),
          },
        },
        hasMerkzeichenAg: {
          ...fields.personBHasMerkzeichenAg,
          name: "person_b_has_merkzeichen_ag",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenAg.label"),
          },
        },
        hasMerkzeichenBl: {
          ...fields.personBHasMerkzeichenBl,
          name: "person_b_has_merkzeichen_bl",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenBl.label"),
          },
        },
        hasMerkzeichenTbl: {
          ...fields.personBHasMerkzeichenTbl,
          name: "person_b_has_merkzeichen_tbl",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenTbl.label"),
          },
        },
        hasMerkzeichenH: {
          ...fields.personBHasMerkzeichenH,
          name: "person_b_has_merkzeichen_h",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenH.label"),
          },
        },
      }}
    />
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
