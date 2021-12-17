import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { selectionFieldPropType } from "../lib/propTypes";
import FormFieldRadio from "../components/FormFieldRadio";
import Details from "../components/Details";

const DetailsDiv = styled.div`
  margin-bottom: var(--spacing-04);
`;

export default function PauschbetragPagePersonA({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={
          <Trans
            t={t}
            i18nKey="lotse.pauschbetragPersonA.intro"
            components={{
              bold: <b />,
            }}
          />
        }
      />
      <DetailsDiv>
        <Details
          title={t("lotse.pauschbetragPersonA.details.title")}
          detailsId="pauschbetrag_person_a_details"
        >
          {{
            paragraphs: [
              <Trans
                t={t}
                i18nKey="lotse.pauschbetragPersonA.details.p1"
                components={{
                  list: <ul />,
                  listItem: <li />,
                }}
              />,
              t("lotse.pauschbetragPersonA.details.p2"),
              <Trans
                t={t}
                i18nKey="lotse.pauschbetragPersonA.details.p3"
                components={{
                  bold: <b />,
                }}
              />,
              t("lotse.pauschbetragPersonA.details.p4"),
            ],
          }}
        </Details>
      </DetailsDiv>
      <StepForm {...form}>
        <FormFieldRadio
          fieldName="person_a_wants_pauschbetrag"
          fieldId="person_a_wants_pauschbetrag"
          label={{ text: "" }}
          // TODO set text here, not in server
          options={fields.personAWantsPauschbetrag.options}
          value={fields.personAWantsPauschbetrag.selectedValue}
          errors={fields.personAWantsPauschbetrag.errors}
        />
      </StepForm>
    </>
  );
}

PauschbetragPagePersonA.propTypes = {
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
    personAWantsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
