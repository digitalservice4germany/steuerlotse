import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import { fieldPropType } from "../lib/propTypes";
import HasDisabilityPage from "./HasDisabilityPage";

export default function HasDisabilityPersonAPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  numUsers,
}) {
  const { t } = useTranslation();

  const translationBold = function translationBold(key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  let headerIntro = translationBold("lotse.hasDisability.intro_single");

  if (numUsers > 1) {
    headerIntro = translationBold("lotse.hasDisability.intro_person_a");
  }

  return (
    <HasDisabilityPage
      {...{ stepHeader, form, prevUrl }}
      headerIntro={headerIntro}
      fields={{
        hasDisability: {
          ...fields.personAHasDisability,
          name: "person_a_has_disability",
        },
      }}
    />
  );
}

HasDisabilityPersonAPage.propTypes = {
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
    personAHasDisability: fieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  numUsers: PropTypes.number.isRequired,
};
