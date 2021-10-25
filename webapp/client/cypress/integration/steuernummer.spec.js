describe("Steuernummer", () => {
  context("when single", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/familienstand");
      cy.get("label[for=familienstand-0]").click();
      cy.get('[name="next_button"]').click();
    });

    it("displays correct text", () => {
      cy.get("label[for=steuernummer_exists]").contains(
        /^Haben Sie bereits eine Steuernummer/
      );
    });

    it("displays bundesland in dropdown", () => {
      cy.get("label[for=steuernummer_exists-yes]").click();
      cy.get("select[name=bundesland]")
        .children("option[value=BW]")
        .should("exist");
      cy.get("select[name=bundesland]")
        .children("option[value=TH]")
        .should("exist");
    });

    it("displays bufa_nr in dropdown", () => {
      cy.get("label[for=steuernummer_exists-no]").click();
      cy.get("select[name=bundesland]").select("BY");
      cy.get("select[name=bufa_nr]")
        .children("option[value=9201]")
        .should("exist");
      cy.get("select[name=bufa_nr]")
        .children("option[value=9170]")
        .should("exist");
    });
  });

  context("when married", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/familienstand");
      cy.get("label[for=familienstand-1]").click();
      cy.get("#familienstand_date_1").clear().type("1");
      cy.get("#familienstand_date_2").clear().type("1");
      cy.get("#familienstand_date_3").clear().type("1980");
      cy.get("label[for=familienstand_married_lived_separated-no]").click();
      cy.get("label[for=familienstand_confirm_zusammenveranlagung]")
        .first()
        .click();
      cy.get('[name="next_button"]').click();
    });

    it("displays correct text", () => {
      cy.get("label[for=steuernummer_exists]").contains(
        /^Haben Sie bereits eine gemeinsame Steuernummer/
      );
    });
  });
});
