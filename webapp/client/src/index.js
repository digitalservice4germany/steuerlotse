import React from "react";
import ReactDOM from "react-dom";
// TODO: Some components expect bootstrap css to be present. This is currently
// loaded in the jinja template that includes these React components.
import "./lib/i18n";
import LoginPage from "./pages/LoginPage";
import LoginFailurePage from "./pages/LoginFailurePage";
import LogoutPage from "./pages/LogoutPage";
import RegistrationPage from "./pages/RegistrationPage";
import RevocationPage from "./pages/RevocationPage";
import RevocationSuccessPage from "./pages/RevocationSuccessPage";
import DeclarationIncomesPage from "./pages/DeclarationIncomesPage";
import SessionNotePage from "./pages/SessionNotePage";
import TaxNumberPage from "./pages/TaxNumberPage";
import TelephoneNumberPage from "./pages/TelephoneNumberPage";
import StmindSelectionPage from "./pages/StmindSelectionPage";
import ConfirmationPage from "./pages/ConfirmationPage";
import HasDisabilityPersonAPage from "./pages/HasDisabilityPersonAPage";
import HasDisabilityPersonBPage from "./pages/HasDisabilityPersonBPage";
import MerkzeichenPersonAPage from "./pages/MerkzeichenPersonAPage";
import MerkzeichenPersonBPage from "./pages/MerkzeichenPersonBPage";
import PauschbetragPersonAPage from "./pages/PauschbetragPersonAPage";
import PauschbetragPersonBPage from "./pages/PauschbetragPersonBPage";
import FahrtkostenpauschalePersonAPage from "./pages/FahrtkostenpauschalePersonAPage";
import FahrtkostenpauschalePersonBPage from "./pages/FahrtkostenpauschalePersonBPage";
import NoPauschbetragPage from "./pages/NoPauschbetragPage";
import DeclarationEDatenPage from "./pages/DeclarationEDatenPage";
import UnlockCodeSuccessPage from "./pages/UnlockCodeSuccessPage";
import UnlockCodeFailurePage from "./pages/UnlockCodeFailurePage";
import RevocationFailurePage from "./pages/RevocationFailurePage";
import SubmitAcknowledgePage from "./pages/SubmitAcknowledgePage";
import FilingSuccessPage from "./pages/FilingSuccessPage";
import FilingFailurePage from "./pages/FilingFailurePage";
import InfoTaxReturnForPensionersPage from "./pages/InfoTaxReturnForPensionersPage";
import MedicalExpensesInfoPage from "./pages/MedicalExpensesInfoPage";
import PensionExpensesInfoPage from "./pages/PensionExpensesInfoPage";
import DisabilityCostsInfoPage from "./pages/DisabilityCostsInfoPage";
import CareCostsInfoPage from "./pages/CareCostsInfoPage";
import FuneralExpensesInfoPage from "./pages/FuneralExpensesInfoPage";
import VorbereitenOverviewPage from "./pages/VorbereitenOverviewPage";
import HouseholdServicesInfoPage from "./pages/HouseholdServicesInfoPage";
import ReplacementCostsInfoPage from "./pages/ReplacementCostsInfoPage";
import DonationInfoPage from "./pages/DonationInfoPage";
import ChurchTaxInfoPage from "./pages/ChurchTaxInfoPage";
import CraftsmanServicesInfoPage from "./pages/CraftsmanServicesInfoPage";
import InfoForRelativesPage from "./pages/InfoForRelativesPage";
import SummaryPage from "./pages/SummaryPage";
import LandingPage from "./pages/LandingPage";
import NewsletterSuccessPage from "./pages/NewsletterSuccessPage";
import NewsletterRegisterBox from "./components/NewsletterRegisterBox";
import FreeTaxDeclarationForPensionersPage from "./pages/FreeTaxDeclarationForPensionersPage";
import MandateForTaxDeclarationPage from "./pages/MandateForTaxDeclarationPage";

const allowedComponents = {
  RegistrationPage,
  LoginPage,
  LoginFailurePage,
  LogoutPage,
  RevocationPage,
  RevocationSuccessPage,
  RevocationFailurePage,
  UnlockCodeSuccessPage,
  UnlockCodeFailurePage,
  DeclarationIncomesPage,
  SessionNotePage,
  DeclarationEDatenPage,
  TaxNumberPage,
  HasDisabilityPersonAPage,
  MerkzeichenPersonAPage,
  PauschbetragPersonAPage,
  FahrtkostenpauschalePersonAPage,
  HasDisabilityPersonBPage,
  MerkzeichenPersonBPage,
  PauschbetragPersonBPage,
  FahrtkostenpauschalePersonBPage,
  NoPauschbetragPage,
  TelephoneNumberPage,
  StmindSelectionPage,
  ConfirmationPage,
  FilingSuccessPage,
  FilingFailurePage,
  SubmitAcknowledgePage,
  InfoTaxReturnForPensionersPage,
  MedicalExpensesInfoPage,
  PensionExpensesInfoPage,
  DisabilityCostsInfoPage,
  CareCostsInfoPage,
  FuneralExpensesInfoPage,
  VorbereitenOverviewPage,
  HouseholdServicesInfoPage,
  ReplacementCostsInfoPage,
  DonationInfoPage,
  ChurchTaxInfoPage,
  CraftsmanServicesInfoPage,
  InfoForRelativesPage,
  SummaryPage,
  LandingPage,
  NewsletterSuccessPage,
  NewsletterRegisterBox,
  FreeTaxDeclarationForPensionersPage,
  MandateForTaxDeclarationPage,
};

function mountComponent(element) {
  const name = element.dataset.componentName;
  const Component = allowedComponents[name];
  if (Component !== undefined) {
    const props = element.dataset.propsJson
      ? JSON.parse(element.dataset.propsJson)
      : {};
    ReactDOM.render(
      <React.StrictMode>
        <Component {...props} />
      </React.StrictMode>,
      element
    );
  } else {
    // TODO: Consider integrating an error reporting service.
    // eslint-disable-next-line
    console.log(`No such component "${name}"`);
  }
}

document.querySelectorAll("[data-is-component=yes]").forEach(mountComponent);
