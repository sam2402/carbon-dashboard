
import { tokens } from "../../theme";
import { Box, Typography, useTheme} from "@mui/material";
import Header from "../../components/Header";

import LineChartRealTime from "../../components/LineChart/LineChartRealTime";
import BarChartRealTime from "../../components/BarChart/BarChartRealTime";
import PieChartRealTime from "../../components/PieChart/PieChartRealTime";


const RealTime = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box m="20px">
      <Header title="REAL TIME USAGE" subtitle="Time Span of last 24 hours" />
      
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
            <LineChartRealTime />
          </Box>
        </Box>


        {/* ROW 2 */}

        <Box
          gridColumn="span 7"
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
            <BarChartRealTime />
          </Box>
        </Box>

        <Box
          gridColumn="span 5"
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
            <PieChartRealTime  />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default RealTime;
