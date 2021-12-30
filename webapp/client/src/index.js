import React from "react";
import ReactDOM from "react-dom";
// TODO: Some components expect bootstrap css to be present. This is currently
// loaded in the jinja template that includes these React components.
import "./lib/i18n";
import LoginPage from "./pages/LoginPage";
import LoginFailurePage from "./pages/LoginFailurePage";
import RegistrationPage from "./pages/RegistrationPage";
import RevocationPage from "./pages/RevocationPage";
import RevocationSuccessPage from "./pages/RevocationSuccessPage";
import DeclarationIncomesPage from "./pages/DeclarationIncomesPage";
import TaxNumberPage from "./pages/TaxNumberPage";
import TelephoneNumberPage from "./pages/TelephoneNumberPage";
import StmindSelectionPage from "./pages/StmindSelectionPage";
import ConfirmationPage from "./pages/ConfirmationPage";
import PersonAHasDisabilityPage from "./pages/PersonAHasDisabilityPage";
import PersonBHasDisabilityPage from "./pages/PersonBHasDisabilityPage";
import PauschbetragPersonAPage from "./pages/PauschbetragPersonAPage";
import PauschbetragPersonBPage from "./pages/PauschbetragPersonBPage";
import FahrkostenpauschalePersonAPage from "./pages/FahrkostenpauschalePersonAPage";
import FahrkostenpauschalePersonBPage from "./pages/FahrkostenpauschalePersonBPage";

const allowedComponents = {
  RegistrationPage,
  LoginPage,
  LoginFailurePage,
  RevocationPage,
  RevocationSuccessPage,
  DeclarationIncomesPage,
  TaxNumberPage,
  PersonAHasDisabilityPage,
  PauschbetragPersonAPage,
  FahrkostenpauschalePersonAPage,
  PersonBHasDisabilityPage,
  PauschbetragPersonBPage,
  FahrkostenpauschalePersonBPage,
  TelephoneNumberPage,
  StmindSelectionPage,
  ConfirmationPage,
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
