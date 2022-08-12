describe("Landing page", () => {
  it("Clicking button should not be possible", () => {
    cy.visit("/");
    // Button is disabled
    cy.get("a").contains("Jetzt prüfen").should("have.attr", "disabled");
    cy.get("a")
      .contains("Jetzt prüfen")
      .should("have.css", "pointer-events", "none");
    cy.get("a")
      .contains("Jetzt prüfen")
      .should("have.css", "cursor", "default");
  });

  it("eligibility process should be disabled", () => {
    cy.get("span")
      .contains(/^Nutzung prüfen$/)
      .should("have.class", "inactive");
  });

  it("registration should be disabled", () => {
    cy.get("span")
      .contains(/^Registrieren$/)
      .should("have.class", "inactive");
  });
});
