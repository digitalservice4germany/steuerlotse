import "bootstrap/dist/css/bootstrap.css";
import "./../src/storybook-assets/variables.css";
import "./../src/storybook-assets/base.css";

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
};
