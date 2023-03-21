import React from "react";
import {
  Box,
  Container,
  Row,
  Column,
  FooterLink,
  Heading,
} from "./FooterStyles";

const Footer = () => {

  return (
      <Box 
        display="flex" 
        justifyContent="space-between"
        >
        <h4 style={{ color: "White", 
                    textAlign: "center", 
                    marginTop: "-40px",
                    fontFamily:"Arial"}}>
          Volvo - "We make cars for people who care about other people."
        </h4>
      <Container >
        <Row>
          <Column>
            <Heading>About Us</Heading>
            <FooterLink href="https://greensoftware.foundation/">Green Software Foundation</FooterLink>
            <FooterLink href="https://www.volvogroup.com/en/about-us/our-mission-vison-and-aspirations.html">Vision</FooterLink>
            <FooterLink href="https://www.avanade.com/en-ca/media-center/press-releases/volvo-wins-do-what-matters-sustainability-award">Avanade</FooterLink>
          </Column>
          <Column>
            <Heading>Social Media</Heading>
            <FooterLink href="https://www.facebook.com/volvogroup/">
              <i className="fab fa-facebook-f">
                <span style={{ marginLeft: "10px" }}>
                  Facebook
                </span>
              </i>
            </FooterLink>
            <FooterLink href="https://www.instagram.com/volvogroup/?hl=en">
              <i className="fab fa-instagram">
                <span style={{ marginLeft: "10px" }}>
                  Instagram
                </span>
              </i>
            </FooterLink>
            <FooterLink href="https://twitter.com/VolvoGroup?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor">
              <i className="fab fa-twitter">
                <span style={{ marginLeft: "10px" }}>
                  Twitter
                </span>
              </i>
            </FooterLink>
          </Column>
        </Row>
      </Container>
        
      </Box>

   
  );
};

export default Footer;
