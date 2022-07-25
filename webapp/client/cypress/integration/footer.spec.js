describe("Footer", () => {
  beforeEach(() => {
    cy.visit("/");
  });
  it("Clicking link to Kontact page", () => {
    cy.get("a").contains("Kontakt und Feedback").click();

    cy.url().should("include", "/kontakt");
  });

  it("Clicking link to Datenschutzerklärung", () => {
    cy.get("a").contains("Datenschutzerklärung").click();

    cy.url().should("include", "/datenschutz");
  });

  it("link clickable to Freischaltcode stornieren", () => {
    cy.get("a").contains("Freischaltcode stornieren").click();
    cy.url().should("include", "/unlock_code_revocation/step/data_input");
  });

  it("Clicking link to Nutzungsbedingungen", () => {
    cy.get("a").contains("Nutzungsbedingungen").click();

    cy.url().should("include", "/agb");
  });

  it("Clicking link to Impressum", () => {
    cy.get("a").contains("Impressum").click();

    cy.url().should("include", "/impressum");
  });

  it("Clicking link to Erklärung zur Barrierefreiheit", () => {
    cy.get("a").contains("Erklärung zur Barrierefreiheit").click();

    cy.url().should("include", "/barrierefreiheit");
  });
});
