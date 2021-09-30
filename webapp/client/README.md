# Steuerlotse UI components

## Overview

This directory contains a React app with components for use in the Steuerlotse webapp.

We have two types of components:

- `src/pages/`: page components that represent e.g. the login page or an individual form step in the application and are included from jinja templates.
- `src/components/`: a library of shared UI components that make up the individual pages. Think of this as the Steuerlotse component library.

Other directories:

- `.storybook/`: configures the environment in which components get rendered in Storybook.
- `public/`: static assets that get served as-is.
- `src/assets/`: any static assets that are used by the components and get processed by webpack.
- `src/lib`: any non-component JS.
- `src/storybook-assets`: special assets folder just used by Storybook - it cannot include the files in `public/`.

## Using components from Flask (jinja) templates

When this React app is loaded on a page, it scans for elements that have these attributes set:

```html
<div
  data-is-component="yes"
  data-component-name="MyComponent"
  data-props-json="{{ {} | tojson | forceescape }}"
></div>
```

For each such element, it mounts the corresponding React component and populates it with the provided props.

## Developing

### `yarn storybook`

Runs storybook. Builds and reloads components as you edit them. Shows lint errors in the console.

This is the recommended way to develop pages and components: Storybook allows you to look at your components in isolation and show their various states by writing ["Stories"](https://storybook.js.org/docs/react/get-started/whats-a-story) for the component (e.g. different button styles or form fields with vs. without errors).

### `yarn start`

Runs the app in the development mode on [http://localhost:3000](http://localhost:3000). Reloads components as you edit them. Shows lint errors in the console.

This serves up JS/CSS/etc from the React app and proxies everything else to `localhost:5000`, where it expects the Flask app to be running. See `src/setupProxy.js` for details on what is being proxied.

### Testing

#### `yarn test`

Launches the unit test runner in the interactive watch mode. See [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

#### `yarn test:functional`

Runs functional tests which exercise both the flask app and the client-side components in a real browser environment.

#### `yarn cypress`

Opens the Cypress test runner UI. [See here for details](https://docs.cypress.io/guides/core-concepts/test-runner).

### `yarn lint`

Runs eslint and shows information about coding errors.

### `yarn prepare`

Installs a pre-commit hook that automatically formats JS and CSS files before writing commits. You only need to run this once when you check out the repository for the first time.

### `yarn format`

Auto-format JS and CSS files. You do not need to run this manually unless you want to view the results before committing.

### `yarn build`

Builds the app for production to the `build` folder. You generally don't need to do this - it happens automatically in the deploy pipeline.

## Tools and technologies used

- [React](https://reactjs.org/)
- This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app) (CRA).
- CRA configuration is extended using [react-app-rewired](https://github.com/timarney/react-app-rewired).
- [yarn](https://yarnpkg.com/) for package management.
- [Styled-Components](https://styled-components.com/) for keeping styles close to the components they style.
- [i18next](https://www.i18next.com/) and [react-i18next](https://react.i18next.com/) for managing text strings.
- [eslint](https://eslint.org/) for finding errors early using static analysis.
- [prettier](https://prettier.io/) to enforce a coding style with a pre-commit hook, so that a) our code has a consistent look and b) we don't ever have to argue about what that should be.
- Testing
  - [Testing Library](https://testing-library.com/docs) for component tests, see:
    - [Testing Library Queries](https://testing-library.com/docs/queries/about) and [Events](https://testing-library.com/docs/dom-testing-library/api-events).
    - [Jest](https://jestjs.io/) [global functions](https://jestjs.io/docs/api) and [matchers](https://jestjs.io/docs/expect) as well as [additional DOM matchers](https://github.com/testing-library/jest-dom).
  - [Cypress](https://docs.cypress.io/) for end-to-end tests.
- [Storybook](https://storybook.js.org/) for developing and demonstrating UI components in isolation.
