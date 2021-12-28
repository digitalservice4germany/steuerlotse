import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormHeader from "../components/FormHeader";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";
import { fieldPropType } from "../lib/propTypes";

const DetailsDiv = styled.div`
  margin-bottom: var(--spacing-04);

  @media (max-width: 500px) {
    margin-bottom: 0;
  }
`;

export default function HasDisabilityPersonAPage({
  form,
  fields,
  prevUrl,
  stepHeader,
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
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader title={stepHeader.title} intro={headerIntro} />
      <StepForm {...form}>
        <DetailsDiv>
          <Details
            title={t("lotse.hasDisability.details.title")}
            detailsId="person_a_has_disability_detail"
          >
            {translationBold("lotse.hasDisability.details.text")}
          </Details>
        </DetailsDiv>
        <FormFieldRadioGroup
          fieldId="person_a_has_disability"
          fieldName="person_a_has_disability"
          options={[
            {
              value: "yes",
              displayName: t("fields.yesNoSwitch.Yes"),
            },
            {
              value: "no",
              displayName: t("fields.yesNoSwitch.No"),
            },
          ]}
          value={fields.personAHasDisability.value}
          errors={fields.personAHasDisability.errors}
          required
        />
      </StepForm>
    </>
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
  numUsers: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
