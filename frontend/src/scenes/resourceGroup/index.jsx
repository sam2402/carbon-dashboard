import { Box, useTheme, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";
import { useState, useEffect } from "react";

const ResourceGroup = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const resourceGroups = ["EmTech_RAE", "UCL_Water_Beats", "UKI_DAI_DataEngineering_Discovery"];

  const [resourceGroup, setResourceGroup] = useState("EmTech_RAE")

  const [energyTypeAdvice, setEnergyTypeAdvice] = useState("Loading...");
  const [locationAdvice, setLocationAdvice] = useState("Loading...")
  const [resourceConfigurationAdvice, setResourceConfigurationAdvice] = useState("Loading...")
  const [coolingTypeAdvice, setCoolingTypeAdvice] = useState("Loading...")

  useEffect(() => {

    setEnergyTypeAdvice("Loading...")
    setLocationAdvice("Loading...")
    setResourceConfigurationAdvice("Loading...")
    setCoolingTypeAdvice("Loading...")

    const adviceTypes = {
      "energyType": setEnergyTypeAdvice,
      "location": setLocationAdvice,
      "resourceConfiguration": setResourceConfigurationAdvice,
      "coolingType": setCoolingTypeAdvice
    }

    Object.keys(adviceTypes).forEach(adviceType => {
      fetch("http://127.0.0.1:5000/advice?"+ new URLSearchParams({
        resourceGroup: resourceGroup,
        adviceType: adviceType,
      }))
      .then( res =>  res.json() )
      .then(res => {
        console.log(res.value[adviceType][0].trim())
        adviceTypes[adviceType](res.value[adviceType][0].trim())
      })
      .catch(err => {
        console.log(err)
      })
    });
    
  }, [resourceGroup])


  return (
    <Box m="20px">
      <Header title="Resource Group" subtitle="Advice for a specific resource group" />

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

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Energy Type
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography style={{whiteSpace: 'pre-line'}}>
            {energyTypeAdvice}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Location
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography style={{whiteSpace: 'pre-line'}}>
            <strong>Suggested location for resources:</strong>
            {"\n"+locationAdvice}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Resources Configuration
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography style={{whiteSpace: 'pre-line'}}>
            {resourceConfigurationAdvice}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Cooling Type
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography style={{whiteSpace: 'pre-line'}}>
            {coolingTypeAdvice}
          </Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default ResourceGroup;