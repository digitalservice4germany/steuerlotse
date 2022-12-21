describe("Info page", () => {
  it("Clicking button in main page should not be possible", () => {
    cy.visit("/vorbereiten");
    // Button is disabled
    cy.get("a").contains("Jetzt anmelden").should("have.attr", "disabled");
    cy.get("a")
      .contains("Jetzt anmelden")
      .should("have.css", "pointer-events", "none");
    cy.get("a")
      .contains("Jetzt anmelden")
      .should("have.css", "cursor", "default");
  });

  it("Clicking button in all info sub pages should not be possible", () => {
    cy.get('a[class^="TileCard"]').each(($row) => {
      const href = $row.attr("href");
      cy.visit(href);
      cy.url().should("include", href);
      // Button is disabled
      cy.get("a").contains("Jetzt anmelden").should("have.attr", "disabled");
      cy.get("a")
        .contains("Jetzt anmelden")
        .should("have.css", "pointer-events", "none");
      cy.get("a")
        .contains("Jetzt anmelden")
        .should("have.css", "cursor", "default");
    });
  });
});
