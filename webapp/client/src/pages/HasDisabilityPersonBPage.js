import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import { fieldPropType } from "../lib/propTypes";
import HasDisabilityPage from "./HasDisabilityPage";

export default function HasDisabilityPersonBPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  plausibleDomain,
}) {
  const { t } = useTranslation();
  const plausibleProps = {
    method: "Behinderung oder Pflegebedürftigkeit für Person B",
  };

  const translationBold = function translationBold(key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  return (
    <HasDisabilityPage
      plausibleDomain={plausibleDomain}
      plausibleProps={plausibleProps}
      {...{ stepHeader, form, prevUrl }}
      headerIntro={translationBold("lotse.hasDisability.intro_person_b")}
      fields={{
        hasDisability: {
          ...fields.personBHasDisability,
          name: "person_b_has_disability",
        },
      }}
    />
  );
}

HasDisabilityPersonBPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personBHasDisability: fieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

HasDisabilityPersonBPage.defaultProps = {
  plausibleDomain: null,
};
