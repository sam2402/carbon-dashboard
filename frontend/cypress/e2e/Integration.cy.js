import '@testing-library/cypress/add-commands';

describe("Future Prediction Page", () => {
    beforeEach(() => {
      cy.visit("http://localhost:3000/futurePred");
    });
  
    it("Access Future Prediction Page", () => {
      cy.findByText("FUTURE PREDICTION").should("exist");
    });
    
    it("Resource Groups\' EmTech_RAE \' rendered properly in Region page", () => {
        cy.findByLabelText('Resource Group').click()
        cy.findByRole('option', { name: /EmTech_RAE/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'EmTech_RAE');
    });

    it("Resource Groups rendered properly in Future page", () => {
        cy.findByLabelText('Resource Group').click()
        cy.findByRole('option', { name: /UKI_DAI_DataEngineering_Discovery/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'UKI_DAI_DataEngineering_Discovery');
    });
  });

describe("Past Usage Page", () => {
    beforeEach(() => {
      cy.visit("http://localhost:3000/pastUsage");
    });
  
    it("Access Past Usage Page", () => {
      cy.findByText("PAST USAGE").should("exist");
    });
    
    it("Resource Groups\' EmTech_RAE \' rendered properly in Region page", () => {
        cy.findByLabelText('Resource Group').click()
        cy.findByRole('option', { name: /EmTech_RAE/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'EmTech_RAE');
    });

    it("Resource Groups rendered properly in Past page", () => {
        cy.findByLabelText('Resource Group').click()
        cy.findByRole('option', { name: /UKI_DAI_DataEngineering_Discovery/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'UKI_DAI_DataEngineering_Discovery');
    });
    });

describe("Resource Group Page", () => {
    beforeEach(() => {
        cy.visit("http://localhost:3000/resourceGroup");
    });
    
    it("Resource Groups\' EmTech_RAE \' rendered properly in Region page", () => {
        cy.findByLabelText('Resource Group').click()
        cy.findByRole('option', { name: /EmTech_RAE/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'EmTech_RAE');
    });

    it("Resource Groups\' UKI_DAI_DataEngineering_Discovery \' rendered properly in Region page", () => {
        cy.findByLabelText('Resource Group').click()
        cy.findByRole('option', { name: /UKI_DAI_DataEngineering_Discovery/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'UKI_DAI_DataEngineering_Discovery');
    });
});
    
describe("Region Page", () => {
    beforeEach(() => {
        cy.visit("http://localhost:3000/region");
    });
            
    it("Resource Groups \' uksouth \' rendered properly in Region page", () => {
        cy.findByLabelText('Region').click()
        cy.findByRole('option', { name: /uksouth/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'uksouth');
    });

    it("Resource Groups \' westeurope \' rendered properly in Region page", () => {
        cy.findByLabelText('Region').click()
        cy.findByRole('option', { name: /westeurope/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'westeurope');
    });
        
    it("Resource Groups \' northeurope \' rendered properly in Region page", () => {
        cy.findByLabelText('Region').click()
        cy.findByRole('option', { name: /northeurope/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'northeurope');
    });
        
    it("Resource Groups \' eastus \'rendered properly in Region page", () => {
        cy.findByLabelText('Region').click()
        cy.findByRole('option', { name: /eastus/i }).click()
        cy.wait(500);
        cy.get('#demo-simple-select').should('contain.text', 'eastus');
    });
});
  