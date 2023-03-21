import { Box, useTheme } from "@mui/material";
import Header from "../../components/Header";
import GeographyChart from "../../components/GeographyChart/GeographyChartRealTime";
import { tokens } from "../../theme";

const Home = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box m="20px">
      <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="125px"
        gap="20px"
      >
        <Box
          height="70vh"
          border={`1px solid ${colors.grey[100]}`}
          borderRadius="4px"
          gridColumn="span 12"
          gridRow="span 6"
        >
          <GeographyChart />
        </Box>   
      </Box>   
    </Box>
  );
};

export default Home;