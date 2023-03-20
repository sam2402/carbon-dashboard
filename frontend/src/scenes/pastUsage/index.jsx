import { Box, Typography, useTheme} from "@mui/material";
import { tokens } from "../../theme";
import LineChartPastUsage from "../../components/LineChart/LineChartPastUsage";
import Header from "../../components/Header";
import PieChartPastUsage from "../../components/PieChart/PieChartPastUsage";
import BarChartPastUsage from "../../components/BarChart/BarChartPastUsage";
import React from "react";
import {
  
  Container,
  Row,
  Column,
  FooterLink,
  Heading,
} from "../global/FooterStyles";


const PastUsage = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box m="20px">
      <Header title="PAST USAGE" subtitle="Time Span of 10 Years in the Past" />
      
      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="125px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box
          gridColumn="span 12"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          
        >
          <Box
            mt="10px"
            p="0 20px"
         
          >
            <Box >
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                Total Carbon Usage
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                21,357,131 Metric Tonnes
              </Typography>
            </Box>
            
          </Box>
          <Box  height="35vh" m="-20px 0 0 0">
            <LineChartPastUsage />
          </Box>
        </Box>

      

        {/* ROW 2 */}

        <Box
          gridColumn="span 8"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}

        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Emissions type per Region
          </Typography>
          <Box height="40vh" mt="-20px">
            <BarChartPastUsage />
          </Box>
        </Box>

        <Box
          gridColumn="span 4"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          padding="20px"

        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ marginBottom: "15px" }}
          >
            Scopes of Emissions
          </Typography>
          <Box height="35vh" >
            <PieChartPastUsage  />
          </Box>
        </Box>

        <Box display="flex" justifyContent="space-between">
      <h1 style={{ color: "White", 
                   textAlign: "center", 
                   marginTop: "-50px" }}>
        Volvo - "We make cars for people who care about other people.""
      </h1>
      <Container>
        <Row>
          <Column>
            <Heading>About Us</Heading>
            <FooterLink href="#">Aim</FooterLink>
            <FooterLink href="#">Vision</FooterLink>
            <FooterLink href="#">Testimonials</FooterLink>
          </Column>
          <Column>
            <Heading>Services</Heading>
            <FooterLink href="#">Writing</FooterLink>
            <FooterLink href="#">Internships</FooterLink>
            <FooterLink href="#">Coding</FooterLink>
            <FooterLink href="#">Teaching</FooterLink>
          </Column>
          <Column>
            <Heading>Contact Us</Heading>
            <FooterLink href="#">Uttar Pradesh</FooterLink>
            <FooterLink href="#">Ahemdabad</FooterLink>
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
              <i className="fab fa-instagram">
                <span style={{ marginLeft: "10px" }}>
                  Instagram
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
            <FooterLink href="#">
              <i className="fab fa-youtube">
                <span style={{ marginLeft: "10px" }}>
                  Youtube
                </span>
              </i>
            </FooterLink>
          </Column>
        </Row>
      </Container>
      
    </Box>
      </Box>
    </Box>
  );
};

export default PastUsage ;
