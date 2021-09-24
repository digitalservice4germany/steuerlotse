import "./../src/lib/i18n";
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

// Add render context from app/templates/basis/base.html
export const decorators = [
  (Story) => (
    <div className="main-content">
      <div className="mt-4">
        <div className="col-lg-9 col-md-10 col-xs-12 p-0">
          <Story />
        </div>
      </div>
    </div>
  ),
];
