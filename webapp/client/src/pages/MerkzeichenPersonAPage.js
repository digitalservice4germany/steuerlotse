import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import { checkboxPropType, fieldPropType } from "../lib/propTypes";
import MerkzeichenPage from "./MerkzeichenPage";

export default function MerkzeichenPersonAPage({
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
          ...fields.personAHasPflegegrad,
          name: "person_a_has_pflegegrad",
          label: {
            text: t("lotse.merkzeichen.hasPflegegrad.label"),
          },
        },
        disabilityDegree: {
          ...fields.personADisabilityDegree,
          name: "person_a_disability_degree",
          label: {
            text: t("lotse.merkzeichen.disabilityDegree.label"),
            exampleInput: t("lotse.merkzeichen.disabilityDegree.example"),
          },
        },
        hasMerkzeichenG: {
          ...fields.personAHasMerkzeichenG,
          name: "person_a_has_merkzeichen_g",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenG.label"),
          },
        },
        hasMerkzeichenAg: {
          ...fields.personAHasMerkzeichenAg,
          name: "person_a_has_merkzeichen_ag",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenAg.label"),
          },
        },
        hasMerkzeichenBl: {
          ...fields.personAHasMerkzeichenBl,
          name: "person_a_has_merkzeichen_bl",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenBl.label"),
          },
        },
        hasMerkzeichenTbl: {
          ...fields.personAHasMerkzeichenTbl,
          name: "person_a_has_merkzeichen_tbl",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenTbl.label"),
          },
        },
        hasMerkzeichenH: {
          ...fields.personAHasMerkzeichenH,
          name: "person_a_has_merkzeichen_h",
          label: {
            text: t("lotse.merkzeichen.hasMerkzeichenH.label"),
          },
        },
      }}
    />
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
