describe("Registration", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_request/step/data_input");
  });

  it("submitting an empty form", () => {
    // Submit empty form
    cy.get("button[type=submit]").contains("Registrieren").click();

    // Should have errors in the right places.
    cy.get("[role=alert][for=dob]").contains("Dieses Feld wird benötigt");
    cy.get("[role=alert][for=idnr]").contains("Dieses Feld wird benötigt");
    cy.get("[role=alert][for=registration_confirm_data_privacy]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
    cy.get("[role=alert][for=registration_confirm_terms_of_service]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
    cy.get("[role=alert][for=registration_confirm_incomes]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
    cy.get("[role=alert][for=registration_confirm_e_data]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
  });

  it("submitting a complete and correct form", () => {
    cy.fixture("user").then("user", (user) => {
      // Fill DOB
      cy.get("input[id=dob_1]").type("3");
      cy.get("input[id=dob_2]").type("11");
      cy.get("input[id=dob_3]").type("1978");

      // Fill tax ID
      cy.get("input[id=idnr_1]").type("04");
      cy.get("input[id=idnr_2]").type("531");
      cy.get("input[id=idnr_3]").type("672");
      cy.get("input[id=idnr_4]").type("808");

      // Check boxes
      cy.get("label[for=registration_confirm_data_privacy].checkmark").click();
      cy.get(
        "label[for=registration_confirm_terms_of_service].checkmark"
      ).click();
      cy.get("label[for=registration_confirm_incomes].checkmark").click();
      cy.get("label[for=registration_confirm_e_data].checkmark").click();

      // Submit
      cy.get("button[type=submit]").contains("Registrieren").click();

      // Should see success message
      cy.url().should(
        "include",
        "/unlock_code_request/step/unlock_code_success"
      );
    });
  });
});
