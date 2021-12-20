import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import FormFieldRadio from "../components/FormFieldRadio";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";
import { fieldPropType } from "../lib/propTypes";

export default function PersonAHasDisabilityPage({
  form,
  fields,
  prevUrl,
  stepHeader,
  numOfUsers,
}) {
  const { t } = useTranslation();

  const tbold = function (key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  let headerIntro = tbold("lotse.hasDisability.intro_1");

  if (numOfUsers > 1) {
    headerIntro = tbold("lotse.hasDisability.intro_2");
  }

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader title={stepHeader.title} intro={headerIntro} />
      <StepForm {...form}>
        <Details
          title={t("lotse.hasDisability.details.title")}
          detailsId="person_a_has_disability"
        >
          {{
            paragraphs: [tbold("lotse.hasDisability.details.text")],
          }}
        </Details>
        <FormFieldRadio
          fieldId="person_a_has_disability"
          fieldName="person_a_has_disability"
          options={[
            {
              value: "yes",
              displayName: t("fields.switch.Yes"),
            },
            {
              value: "no",
              displayName: t("fields.switch.No"),
            },
          ]}
          value={fields.personA_hasDisability.value}
          errors={fields.personA_hasDisability.errors}
          required
        />
      </StepForm>
    </>
  );
}

PersonAHasDisabilityPage.propTypes = {
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
    personA_hasDisability: fieldPropType,
  }).isRequired,
  numOfUsers: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
