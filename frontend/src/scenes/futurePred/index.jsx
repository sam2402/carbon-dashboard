import { Box, useTheme, Select, FormControl, MenuItem, InputLabel, Typography } from "@mui/material";
import { tokens } from "../../theme";
import LineChartFuturePred from "../../components/LineChart/LineChartFuturePred";
import Header from "../../components/Header";
import React, { useState } from 'react';

const FuturePred = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const resourceGroups = ["EmTech_RAE", "UCL_Water_Beats", "UKI_DAI_DataEngineering_Discovery"];
  const [resourceGroup, setResourceGroup] = useState(["EmTech_RAE"]);

  return (
    <Box m="20px">
      <Header title="FUTURE PREDICTION" subtitle="Next 3 Days" />

      <FormControl style = {{paddingBottom: "30px"}} fullWidth>
        <InputLabel id="demo-simple-select-label">Resource Group</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={resourceGroup}
          label="Resource Group"
          onChange= {(event) => setResourceGroup(event.target.value)}
        >
          {resourceGroups.map(resourceGroup =>
            <MenuItem key={resourceGroup} value={resourceGroup}>{resourceGroup}</MenuItem>
          )}
        </Select>
      </FormControl>
      
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
                Future Emissions by Resource
              </Typography>
            </Box>
            
          </Box>
          <Box  height="45vh" m="-30px 0 0 0">
            <LineChartFuturePred resourceGroup={resourceGroup} />
          </Box>
        </Box>


        {/* ROW 2 */}

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
                Future Emissions by Location
              </Typography>
            </Box>
            
          </Box>
          <Box  height="45vh" m="-30px 0 0 0">
            <LineChartFuturePred resourceGroup={resourceGroup} />
          </Box>
        </Box>
      
      </Box>
    </Box>
  );
  
  
};

export default FuturePred;
