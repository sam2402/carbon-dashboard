import { useTheme } from "@mui/material";
import { useContext } from "react";
import { ColorModeContext } from "../../theme";

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
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);

  return (
      <Box 
        display="flex" 
        justifyContent="space-between"
        >
        <h4 style={{ color: "White", 
                    textAlign: "center", 
                    marginTop: "-40px" }}>
          Volvo - "We make cars for people who care about other people."
        </h4>
        <Container>
          <Row>
            <Column>
              <Heading>About Us</Heading>
              <FooterLink href="#">Aim</FooterLink>
              <FooterLink href="#">Vision</FooterLink>
              <FooterLink href="#">Testimonials</FooterLink>
            </Column>
            <Column>
              <Heading>Contact Us</Heading>
              <FooterLink href="#">UCL</FooterLink>
              <FooterLink href="#">Avanade</FooterLink>
              <FooterLink href="#">Volvo</FooterLink>
            </Column>
            <Column>
              <Heading>Social Media</Heading>
              <FooterLink href="#">
                <i className="fab fa-facebook-f">
                  <span style={{ marginLeft: "10px" }}>
                    Facebook
                  </span>
                </i>
              </FooterLink>
              <FooterLink href="#">
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
