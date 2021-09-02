import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import LoginPage from './pages/LoginPage';

const componentNameMap = {
  'LoginPage': LoginPage
}

function mountComponent(element) {
  const name = element.dataset.componentName;
  const Component = componentNameMap[name];
  if (Component !== undefined) {
    const props = element.dataset.propsJson ? JSON.parse(element.dataset.propsJson) : {}
    ReactDOM.render(
      <React.StrictMode>
        <Component {...props} />
      </React.StrictMode>,
      element
    );
  } else {
    console.log(`No such component "${name}"`)
  }
}

document.querySelectorAll('[data-is-component=yes]').forEach(mountComponent);
