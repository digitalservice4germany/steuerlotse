import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormHeader from "../components/FormHeader";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";
import { extendedFieldPropType } from "../lib/propTypes";

const DetailsDiv = styled.div`
  margin-bottom: var(--spacing-04);

  @media (max-width: 500px) {
    margin-bottom: 0;
  }
`;

export default function HasDisabilityPage({
  form,
  fields,
  stepHeader,
  headerIntro,
  prevUrl,
}) {
  const { t } = useTranslation();

  const translationBold = function translationBold(key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };
  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader title={stepHeader.title} intro={headerIntro} />
      <StepForm {...form}>
        <DetailsDiv>
          <Details
            title={t("lotse.hasDisability.details.title")}
            detailsId={`${fields.hasDisability.name}_detail`}
          >
            {translationBold("lotse.hasDisability.details.text")}
          </Details>
        </DetailsDiv>
        <FormFieldRadioGroup
          fieldId={fields.hasDisability.name}
          fieldName={fields.hasDisability.name}
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
          value={fields.hasDisability.value}
          errors={fields.hasDisability.errors}
          required
        />
      </StepForm>
    </>
  );
}

HasDisabilityPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  headerIntro: PropTypes.oneOfType([PropTypes.string, PropTypes.object])
    .isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    hasDisability: extendedFieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
