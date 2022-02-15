describe("Steuernummer", () => {
  context("when single", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/familienstand");
      cy.extended_footer_is_disabled(true);
      cy.get("label[for=familienstand-0]").click();
      cy.get('[name="next_button"]').click();
    });

    it("displays correct single text for tax number exists question", () => {
      cy.get("#steuernummer_exists")
        .find("legend")
        .contains(/^Haben Sie bereits eine Steuernummer/);
    });

    it("displays correct single text for confirmation field", () => {
      cy.get("label[for=steuernummer_exists-no]").click();
      cy.get("select[name=bundesland]").select("BY");
      cy.get("select[name=bufa_nr]").select("9201");
      cy.get("label[for=request_new_tax_number]").contains(
        /^Hiermit bestätige ich/
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

    it("displays confirmation field", () => {
      cy.get("label[for=steuernummer_exists-no]").click();
      cy.get("select[name=bundesland]").select("BY");
      cy.get("select[name=bufa_nr]").select("9201");
      cy.get("label[for=request_new_tax_number]").should("exist");
    });

    it("displays tax number input", () => {
      cy.get("label[for=steuernummer_exists-yes]").click();
      cy.get("select[name=bundesland]").select("BY");
      cy.get("input[name=steuernummer]").should("exist");
    });
  });

  context("when married", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/familienstand");
      cy.extended_footer_is_disabled(true);
      cy.get("label[for=familienstand-1]").click();
      cy.get("#familienstand_date_1").type("1");
      cy.get("#familienstand_date_2").type("1");
      cy.get("#familienstand_date_3").type("1980");
      cy.get("label[for=familienstand_married_lived_separated-no]").click();
      cy.get("label[for=familienstand_confirm_zusammenveranlagung]")
        .first()
        .click();
      cy.get('[name="next_button"]').click();
    });

    it("displays correct multiple text for tax number exists question", () => {
      cy.get("#steuernummer_exists")
        .find("legend")
        .contains(/^Haben Sie bereits eine gemeinsame Steuernummer/);
    });

    it("displays correct multiple text for confirmation field", () => {
      cy.get("label[for=steuernummer_exists-no]").click();
      cy.get("select[name=bundesland]").select("BY");
      cy.get("select[name=bufa_nr]").select("9201");
      cy.get("label[for=request_new_tax_number]").contains(
        /^Hiermit bestätigen wir/
      );
    });
  });
});
