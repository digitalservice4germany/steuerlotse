describe("SessionNote with no overview button", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("/lotse/step/session_note");
  });

  it("going to previous page", () => {
    cy.get("a").contains("Zurück").click();
    cy.url().should("include", "/lotse/step/decl_edaten");
  });

  it("going to next page", () => {
    cy.get("button[type=submit]").contains("Weiter").click();
    cy.url().should("include", "/lotse/step/familienstand");
  });

  it("not having overview button", () => {
    cy.get("button[type=submit]").contains("Zurück").should("not.exist");
  });
});

describe("SessionNote with overview button", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("/lotse/step/session_note?link_overview=True");
  });

  it("going to previous page", () => {
    cy.get("a").contains("Zurück").click();
    cy.url().should("include", "/lotse/step/decl_edaten");
  });

  it("going to next page", () => {
    cy.get("button[type=submit]").contains("Weiter").click();
    cy.url().should("include", "/lotse/step/familienstand");
  });

  it("going to overview page", () => {
    cy.get("button[type=submit]").contains("Zurück").click();
    cy.url().should("include", "/lotse/step/summary");
  });
});
