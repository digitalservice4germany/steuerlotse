// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

// Fast login command that circumvents the UI as much as possible.
Cypress.Commands.add("login", () => {
  Cypress.log({
    name: "login",
  });

  cy.visit("/unlock_code_activation/step/data_input");

  cy.get("input[name=csrf_token]").then((input) => {
    const csrf = input.val();
    cy.fixture("user").then((user) => {
      // Make request to set session cookie.
      cy.request({
        method: "POST",
        url: "/unlock_code_activation/step/data_input",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `idnr=${user.idnr[0]}&idnr=${user.idnr[1]}&idnr=${user.idnr[2]}&idnr=${user.idnr[3]}&unlock_code=${user.unlockCode[0]}&unlock_code=${user.unlockCode[1]}&unlock_code=${user.unlockCode[2]}&csrf_token=${csrf}`,
        followRedirect: false,
      }).then((resp) => {
        expect(resp.status).to.eq(302);
        expect(resp.redirectedToUrl).to.contain("/lotse/step/start");
      });
    });
  });
});
