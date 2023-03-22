import { Box, Typography, useTheme, Select, FormControl, MenuItem, InputLabel, capitalize} from "@mui/material";
import { tokens } from "../../theme";
import LineChartPastUsage from "../../components/LineChart/LineChartPastUsage";
import Header from "../../components/Header";
import PieChartPastUsage from "../../components/PieChart/PieChartPastUsage";
import BarChartPastUsage from "../../components/BarChart/BarChartPastUsage";
import React, { useState, useEffect } from 'react';

const PastUsage = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const resourceGroups = ["EmTech_RAE", "UCL_Water_Beats", "UKI_DAI_DataEngineering_Discovery"];
  const [resourceGroup, setResourceGroup] = useState(["EmTech_RAE"]);
  const [totalEmissions, setTotalEmissions] = useState()
  const [emissionsBreakdown, setEmissionsBreakdown] = useState({
    pieChart: [],
    barChart: []
  })

  useEffect(() => {

    setTotalEmissions(undefined)
    fetch("http://127.0.0.1:5000/past-total-emissions/"+resourceGroup)
    .then(res => {
      return res.json()
    })
    .then(result => {
      setTotalEmissions(result.value)
    })

    setEmissionsBreakdown({
      pieChart: [],
      barChart: []
    })
    fetch("http://127.0.0.1:5000/past-emissions-breakdown/"+resourceGroup)
    .then(res => {
      return res.json()
    })
    .then(result => {
      setEmissionsBreakdown({
        pieChart: [
          {
            id: "Renewable",
            label: "Renewable",
            value: result.value.renewablePercentage,
          },
          {
            id: "Non-Renewable",
            label: "Non-Renewable",
            value: Math.round((100-result.value.renewablePercentage) * 10) / 10,
          }
        ],
        barChart: Object.entries(result.value.emissionsBreakdownDetail).map(([location, breakdown]) => ({
          region: location,
          ...Object.fromEntries(
            Object.entries(breakdown).map(([powerType, value]) => [capitalize(powerType), Math.round(value)])
          )
        }))
      })
    })



  }, [resourceGroup])

  return (
    <Box m="20px">
      <Header title="PAST USAGE" subtitle="Past ~30 Days" />

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
                Total Carbon Usage
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                {totalEmissions === undefined ? "-" : totalEmissions+"g"}
              </Typography>
            </Box>
            
          </Box>
          <Box  height="45vh" m="-30px 0 0 0">
            <LineChartPastUsage resourceGroup={resourceGroup} />
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
            <BarChartPastUsage data={emissionsBreakdown.barChart}/>
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
            Emission Breakdown
          </Typography>
          <Box height="35vh" >
            <PieChartPastUsage data={emissionsBreakdown.pieChart} />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default PastUsage ;
