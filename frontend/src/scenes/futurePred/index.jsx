import { Box, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import LineChartFuturePred from "../../components/LineChart/LineChartFuturePred";
import Header from "../../components/Header";
import GeographyChartFuturePred from "../../components/GeographyChart/GeographyChartFuturePred";
import BarChartFuturePred from "../../components/BarChart/BarChartFuturePred";
import PieChartFuturePred from "../../components/PieChart/PieChartFuturePred";

const FuturePred = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box m="20px">
      <Header title="FUTURE PREDICTION" subtitle="Time Span of 10 Years into the Future" />
      
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
            <LineChartFuturePred />
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
            <BarChartFuturePred />
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
            <PieChartFuturePred  />
          </Box>
        </Box>
      </Box>
    </Box>
  );
  
  
};

export default FuturePred;
