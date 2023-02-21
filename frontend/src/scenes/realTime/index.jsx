
import { tokens } from "../../theme";
import { Box, Typography, useTheme} from "@mui/material";
import LineChartRealTime from "../../components/LineChart/LineChartRealTime";
import GeographyChart from "../../components/GeographyChart";
import Header from "../../components/Header";
import BarChart from "../../components/BarChart";
import PieChart from "../../components/PieChart";

const RealTime = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box m="20px">
      <Header title="REAL TIME USAGE" subtitle="" />
      
      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="125px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box
          gridColumn="span 6"
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

        
        <Box
          gridColumn="span 6"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          padding="20px"
    
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ marginBottom: "15px" }}
          >
            Geography Based Traffic
          </Typography>
          <Box height="35vh">
            <GeographyChart  />
          </Box>
        </Box>

        {/* ROW 2 */}

        <Box
          gridColumn="span 6"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}

        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Emissions type per continent
          </Typography>
          <Box height="40vh" mt="-20px">
            <BarChart />
          </Box>
        </Box>

        <Box
          gridColumn="span 6"
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
            <PieChart  />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default RealTime;
