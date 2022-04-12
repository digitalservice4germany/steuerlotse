export default function avoidSubmitForm() {
  let emit;

  beforeAll(() => {
    // eslint-disable-next-line no-underscore-dangle
    ({ emit } = window._virtualConsole);
  });

  beforeEach(() => {
    // eslint-disable-next-line no-underscore-dangle
    window._virtualConsole.emit = jest.fn();
  });

  afterAll(() => {
    // eslint-disable-next-line no-underscore-dangle
    window._virtualConsole.emit = emit;
  });
}
