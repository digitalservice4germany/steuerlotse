import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFieldCard from "../components/FormFieldCard";
import vorsorgeIcon from "../assets/icons/vorsorge_icon.svg";
import aussergBelaIcon from "../assets/icons/ausserg_bela_icon.svg";
import handwerkerIcon from "../assets/icons/handwerker_icon.svg";
import spendenIcon from "../assets/icons/spenden_icon.svg";
import religionIcon from "../assets/icons/religion_icon.svg";

export default function StmindSelectionPage({ stepHeader, form, fields }) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormFieldCard
          autofocus
          fieldName="stmind_select_vorsorge"
          fieldId="stmind_select_vorsorge"
          checked={fields.stmind_select_vorsorge.checked}
          labelTitle={t("stmindSelection.selectVorsorge.label.title")}
          labelText={t("stmindSelection.selectVorsorge.label.text")}
          icon={vorsorgeIcon}
          errors={fields.stmind_select_vorsorge.errors}
        />
        <FormFieldCard
          fieldName="stmind_select_ausserg_bela"
          fieldId="stmind_select_ausserg_bela"
          checked={fields.stmind_select_ausserg_bela.checked}
          labelTitle={t("stmindSelection.selectAussergBela.label.title")}
          labelText={t("stmindSelection.selectAussergBela.label.text")}
          icon={aussergBelaIcon}
          errors={fields.stmind_select_ausserg_bela.errors}
        />
        <FormFieldCard
          fieldName="stmind_select_handwerker"
          fieldId="stmind_select_handwerker"
          checked={fields.stmind_select_handwerker.checked}
          labelTitle={t("stmindSelection.selectHandwerker.label.title")}
          labelText={t("stmindSelection.selectHandwerker.label.text")}
          icon={handwerkerIcon}
          errors={fields.stmind_select_handwerker.errors}
        />
        <FormFieldCard
          fieldName="stmind_select_spenden"
          fieldId="stmind_select_spenden"
          checked={fields.stmind_select_spenden.checked}
          labelTitle={t("stmindSelection.selectSpenden.label.title")}
          labelText={t("stmindSelection.selectSpenden.label.text")}
          icon={spendenIcon}
          errors={fields.stmind_select_spenden.errors}
        />
        <FormFieldCard
          fieldName="stmind_select_religion"
          fieldId="stmind_select_religion"
          checked={fields.stmind_select_religion.checked}
          labelTitle={t("stmindSelection.selectReligion.label.title")}
          labelText={t("stmindSelection.selectReligion.label.text")}
          icon={religionIcon}
          errors={fields.stmind_select_religion.errors}
        />
      </StepForm>
    </>
  );
}

const checkboxPropType = PropTypes.exact({
  errors: PropTypes.arrayOf(PropTypes.string),
  checked: PropTypes.bool,
});

StmindSelectionPage.propTypes = {
  stepHeader: PropTypes.exact({
    // TODO: define these here, not in Python
    // render_info.step_title
    title: PropTypes.string,
    // render_info.step_intro
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    // render_info.submit_url
    action: PropTypes.string, // TODO: does this change? if not, define here, not in Python
    // csrf_token()
    csrfToken: PropTypes.string,
    // !!render_info.overview_url
    showOverviewButton: PropTypes.bool,
    // explanatory_button_text
    explanatoryButtonText: PropTypes.string, // TODO: define here, not in Python
    // render_info.additional_info.next_button_label
    nextButtonLabel: PropTypes.string, // TODO: define here, not in Python
  }).isRequired,
  fields: PropTypes.exact({
    stmind_select_vorsorge: checkboxPropType,
    stmind_select_ausserg_bela: checkboxPropType,
    stmind_select_handwerker: checkboxPropType,
    stmind_select_spenden: checkboxPropType,
    stmind_select_religion: checkboxPropType,
  }).isRequired,
};
