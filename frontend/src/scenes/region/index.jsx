import { Box, useTheme, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";
import { useState, useEffect } from "react";

const Region = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [locations, setLocations] = useState([])
  const [location, setLocation] = useState("uksouth")

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

    function getAdvice() {
      Object.entries(adviceTypes).forEach(([adviceType, setAdviceType]) => {
        fetch("http://127.0.0.1:5000/advice?"+ new URLSearchParams({
          azureLocation: location === "" ? locations[0] : location,
          adviceType: adviceType,
        }))
        .then( res =>  res.json() )
        .then(res => {
          setAdviceType(res.value[adviceType][0].trim())
        })
        .catch(err => {
          console.log(err)
        })
      });
    }

    if (locations.length === 0) {
      fetch("http://127.0.0.1:5000/locations")
        .then( res =>  res.json() )
        .then(res => {
          setLocations(res.value)
          getAdvice()
        })
        .catch(err => {
          console.log(err)
        })
      } else {
        getAdvice()
      }
    
  }, [location]) // eslint-disable-line react-hooks/exhaustive-deps


  return (
    <Box m="20px">
      <Header title="Region" subtitle="Advice for a azure region" />

      <FormControl style = {{paddingBottom: "30px"}} fullWidth>
        <InputLabel id="demo-simple-select-label">Region</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={location}
          label="Region"
          onChange= {(event) => setLocation(event.target.value)}
        >
          {locations.map(location =>
            <MenuItem key={location} value={location}>{location}</MenuItem>
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

export default Region;