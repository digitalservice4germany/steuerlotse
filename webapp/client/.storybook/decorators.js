// Add render context from app/templates/basis/base.html
export const baseDecorator = [
  (Story) => (
    <div className="main-content">
      <Story />
    </div>
  ),
];

export const contentPageDecorator = [
  (Story) => (
    <div className="main-content--full-width">
      <Story />
    </div>
  ),
];
