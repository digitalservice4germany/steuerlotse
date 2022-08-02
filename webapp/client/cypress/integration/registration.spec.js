describe("Registration", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_request/step/data_input");
  });

  const loadingSpinnerSelector = '[name="loading_spinner"]';
  const submitBtnSelector = '[name="next_button"]';

  it("submitting an empty form", () => {
    // Submit empty form
    cy.get(loadingSpinnerSelector).should("not.exist");
    cy.get(submitBtnSelector).contains("Registrieren").click();
    cy.get(loadingSpinnerSelector).should("be.visible");

    // Should have errors in the right places.
    cy.get("[role=alert][for=dob]").contains("Geben Sie Ihr Geburtsdatum ein");
    cy.get("[role=alert][for=idnr]").contains(
      "Geben Sie Ihre Steuer-Identifikationsnummer ein"
    );
    cy.get("[role=alert][for=registration_confirm_data_privacy]").contains(
      "Bestätigen Sie, dass Sie mit den Datenschutzrichtlinien einverstanden sind, um fortfahren zu können"
    );
    cy.get("[role=alert][for=registration_confirm_terms_of_service]").contains(
      "Bestätigen Sie, dass Sie den Nutzungbedingungen zustimmen, um fortfahren zu können"
    );
    cy.get("[role=alert][for=registration_confirm_incomes]").contains(
      "Bestätigen Sie, dass Sie die Voraussetzungen zur Nutzung des Steuerlotsen erfüllen, um fortfahren zu können."
    );
    cy.get("[role=alert][for=registration_confirm_e_data]").contains(
      "Bestätigen Sie, dass Sie einverstanden sind, um fortfahren zu können"
    );
  });

  it("submitting a complete and correct form", () => {
    cy.fixture("user").then("user", (_user) => {
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
      cy.get(loadingSpinnerSelector).should("not.exist");
      cy.get(submitBtnSelector).contains("Registrieren").click();
      cy.get(loadingSpinnerSelector).should("be.visible");

      // Should see success message
      cy.url().should(
        "include",
        "/unlock_code_request/step/unlock_code_success"
      );
    });
  });

  it("displaying second waiting message", () => {
    cy.fixture("user").then("user", (_user) => {
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
      cy.get(loadingSpinnerSelector).should("not.exist");

      cy.intercept(
        "/unlock_code_request/step/data_input?link_overview=False",
        (req) => {
          req.on("response", (res) => {
            res.setDelay(11000);
          });
        }
      ).as("makeRegistration");

      cy.get(submitBtnSelector).contains("Registrieren").click();
      cy.get(loadingSpinnerSelector).should("be.visible");
      cy.get('[id="firstMessage"]').should("be.visible");
      cy.get('[id="secondMessage"]').should("not.be.visible");

      cy.wait("@makeRegistration").then(({ _request, _response }) => {
        cy.get('[id="secondMessage"]').should("be.visible");
        cy.get('[id="firstMessage"]').should("not.be.visible");
      });
    });
  });
});
