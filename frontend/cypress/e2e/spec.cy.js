import { Assessment } from '@mui/icons-material';
import'@testing-library/cypress/add-commands';

describe("Test Functional Buttons", () => {
  
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.visit("http://localhost:3000/welcome");
  });

  it("click  Theme Button and check if theme is switched properly", () => {
    
    let afterThemeSwitch = "";

    cy.get('style[data-emotion="css-global"]')
      .should(($style) => {
        const cssText = $style.text();
        if (cssText.includes('body::backdrop{background-color:#141b2d;}')) {
          afterThemeSwitch = 'body::backdrop{background-color:#fcfcfc;}';
        } else {
          afterThemeSwitch = 'body::backdrop{background-color:#141b2d;}';
        }
      });

    cy.get('svg[data-testid="DarkModeOutlinedIcon"] path').click();

    cy.get('style[data-emotion="css-global"]').should(
      'contain.text',
      afterThemeSwitch
    );
    
  });
  
  it("click Menu Button and check if the side bar is hidden", () => {
    
    cy.get('li.pro-menu-item').should('be.visible')
    
    cy.get('svg[data-testid="MenuOutlinedIcon"] path').click()
    
    cy.get('.pro-icon-wrapper').should('exist');
  });
});



describe("Test Page Switch", () => {

  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.visit("http://localhost:3000/welcome");
  });


  it('click Past Usage button and check if it jumps to the correct page', () => {
    cy.get('div.pro-inner-item[tabindex="0"][role="button"] span.pro-item-content a[href="/pastUsage"]').click({force: true})
    cy.url().should('eq', 'http://localhost:3000/pastUsage');
  });

  it('click Future Prediction button and check if it jumps to the correct page', () => {
    cy.get('div.pro-inner-item[tabindex="0"][role="button"] span.pro-item-content a[href="/futurePred"]').click({force: true})
    cy.url().should('eq', 'http://localhost:3000/futurePred');
  })

  it('click Resource Group button and check if it jumps to the correct page', () => {
    cy.get('div.pro-inner-item[tabindex="0"][role="button"] span.pro-item-content a[href="/resourceGroup"]').click({force: true})
    cy.url().should('eq', 'http://localhost:3000/resourceGroup');
  })

  it('click Region button and check if it jumps to the correct page', () => {
    cy.get('div.pro-inner-item[tabindex="0"][role="button"] span.pro-item-content a[href="/region"]').click({force: true})
    cy.url().should('eq', 'http://localhost:3000/region');
  })

});



describe("Test Hidden Information", () => {

  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.visit("http://localhost:3000/welcome");
  });

  it('check if detail descriptions are hidden after clicking hide buttons in resource Group page', () => {
    cy.get('div.pro-inner-item[tabindex="0"][role="button"] span.pro-item-content a[href="/resourceGroup"]').click({force: true})

    cy.get('.MuiAccordionSummary-root')
      .contains('Energy Type')
      .click({ force: true })
    
    cy.get('.MuiAccordionSummary-root')
    .contains('Resources Configuration')
    .click({ force: true })
    
    cy.get('.MuiAccordionSummary-root')
    .contains('Location')
    .click({ force: true })

    cy.get('.MuiAccordionSummary-root')
    .contains('Cooling Type')
    .click({ force: true })

    cy.get('.MuiAccordion-region[role="region"]').should('not.be.visible')
  })

  it('check if detail descriptions are hidden after clicking hide buttons in region page', () => {
    cy.get('div.pro-inner-item[tabindex="0"][role="button"] span.pro-item-content a[href="/region"]').click({force: true})

    cy.get('.MuiAccordionSummary-root')
      .contains('Energy Type')
      .click({ force: true })
    
    cy.get('.MuiAccordionSummary-root')
    .contains('Resources Configuration')
    .click({ force: true })
    
    cy.get('.MuiAccordionSummary-root')
    .contains('Location')
    .click({ force: true })

    cy.get('.MuiAccordionSummary-root')
    .contains('Cooling Type')
    .click({ force: true })

    cy.get('.MuiAccordion-region[role="region"]').should('not.be.visible')
  })

});
