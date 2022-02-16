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
  SubmitAcknowledgePage,
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
