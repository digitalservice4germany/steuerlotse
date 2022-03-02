import PropTypes from "prop-types";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormHeader from "../components/FormHeader";
import DownloadLink from "../components/DownloadLink";
import StepNavButtons from "../components/StepNavButtons";

export default function FilingSuccessPage({
  nextUrl,
  transferTicket,
  downloadUrl,
  taxNumberProvided,
  plausibleDomain,
}) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("filingSuccess.title"),
    intro: t("filingSuccess.intro"),
  };

  // Add custom plausible goal if tax number provided and plausible domain active
  // Hook is called after component is rendered and will only run once after component is rendered
  useEffect(() => {
    if (taxNumberProvided !== null && plausibleDomain !== null) {
      const addPlausibleGoal = () => {
        window.plausible("summary_submitted", {
          props: { tax_number_provided: { taxNumberProvided } },
        });
      };
      document.addEventListener("DOMContentLoaded", addPlausibleGoal);
      // remove listener once the component unmounts
      return () => {
        document.removeEventListener("DOMContentLoaded", addPlausibleGoal);
      };
    }
    return null;
  }, [taxNumberProvided, plausibleDomain]);

  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <h2 className="h4 mt-5">{t("filingSuccess.transfer_ticket.heading")}</h2>
      <p>{t("filingSuccess.transfer_ticket.text")}</p>
      <span className="font-weight-bolder">
        {t("filingSuccess.transfer_ticket.your")} {transferTicket}
      </span>
      <h2 className="h4 mt-5">{t("filingSuccess.pdf.heading")}</h2>
      <p className="mb-4">{t("filingSuccess.pdf.text")}</p>
      <DownloadLink
        text={t("filingSuccess.pdf.download")}
        url={downloadUrl}
        large={false}
      />
      <StepNavButtons nextUrl={nextUrl} isForm={false} />
    </>
  );
}

FilingSuccessPage.propTypes = {
  nextUrl: PropTypes.string.isRequired,
  transferTicket: PropTypes.string.isRequired,
  downloadUrl: PropTypes.string.isRequired,
  taxNumberProvided: PropTypes.bool,
  plausibleDomain: PropTypes.string,
};

FilingSuccessPage.defaultProps = {
  taxNumberProvided: false,
  plausibleDomain: null,
};
