// Add render context from app/templates/basis/base.html
export const baseDecorator = [
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

export const contentPageDecorator = [
  (Story) => (
    <div className="main-content--full-width">
      <div className="mt-4">
        <div className="pt-4 pl-0 pr-0 ml-0 mr-0">
          <Story />
        </div>
      </div>
    </div>
  ),
];
