import React from "react";
import ReactDOM from "react-dom";
// TODO: Some components expect bootstrap css to be present. This is currently
// loaded in the jinja template that includes these React components.
import "./lib/i18n";
import LoginPage from "./pages/LoginPage";

const allowedComponents = {
  LoginPage,
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
