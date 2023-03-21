import { Box, useTheme } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";

const ResourceGroup = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box m="20px">
      <Header title="Resource Group" subtitle="Advice for a particular resource type" />
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Energy Type
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {" \n\nFor the server emtech-rae, it is recommended to reduce reliance on nuclear, coal, oil, and unknown energy sources. It is possible to use more geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server test-ava-rae/ETRAEdb, it is recommended to reduce reliance on coal, oil, and unknown energy sources. It is possible to use more geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server test-ava-rae/ETRAEdbtest, it is recommended to reduce reliance on nuclear, coal, oil, and unknown energy sources. It is possible to use more geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server test-ava-rae/master, it is recommended to reduce reliance on nuclear, coal, and oil energy sources. It is possible to use more geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server test-ava-rae/RAEDb, it is recommended to reduce reliance on coal, oil, and unknown energy sources. It is possible to use more nuclear, geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server raeledgerstorage, it is recommended to reduce reliance on nuclear, geothermal, coal, oil, and unknown energy sources. It is possible to use more biomass, wind, solar, hydro, and battery discharge energy sources, as these have lower emission values. \n\nFor the server raeterraformcodes, it is recommended to reduce reliance on nuclear, geothermal, coal, oil, and unknown energy sources. It is possible to use more biomass, wind, solar, hydro, and battery discharge energy sources, as these have lower emission values. \n\nFor the server opetechrae, it is recommended to reduce reliance on nuclear, coal, oil, and unknown energy sources. It is possible to use more geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server test-emtech-rae-api, it is recommended to reduce reliance on nuclear, coal, oil, and unknown energy sources. It is possible to use more geothermal, biomass, wind, solar, and hydro energy sources, as these have lower emission values. \n\nFor the server ava-emtech-rae, it is recommended to reduce reliance on nuclear, geothermal, coal, oil, and unknown energy sources. It is possible to use more biomass, wind, solar, hydro, and battery discharge energy sources, as these have lower emission values."}
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
          <Typography>
            {"\n\nVolvo server emtech-rae - Suggested Location: Dusseldorf \n\nVolvo server test-ava-rae/ETRAEdb - Suggested Location: Amsterdam \n\nVolvo server test-ava-rae/ETRAEdbtest - Suggested Location: Madrid\n\nVolvo server test-ava-rae/master - Suggested Location: Munich\n\nVolvo server test-ava-rae/RAEDb - Suggested Location: Barcelona \n\nVolvo server raeledgerstorage - Suggested Location: Helsinki\n\nVolvo server raeterraformcodes - Suggested Location: Paris\n\nVolvo server opetechrae - Suggested Location: Copenhagen \n\nVolvo server test-emtech-rae-api - Suggested Location: Stockholm\n\nVolvo server ava-emtech-rae - Suggested Location: Warsaw"}
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
          <Typography>
            {"\n\nSuggestions for Volvo server emtech-rae:\n\n-Intel Xeon E-2186G CPU with a power rating of 95W\n-Intel Xeon E-2176G CPU with a power rating of 80W\n-Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server test-ava-rae/ETRAEdb:\n\n-Intel Xeon E-2186G CPU with a power rating of 95W\n-Intel Xeon E-2176G CPU with a power rating of 80W\n-Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server test-ava-rae/ETRAEdbtest:\n\n-Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server test-ava-rae/master:\n\n-Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server test-ava-rae/RAEDb:\n\n- Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server raeledgerstorage:\n\n- Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server raeterraformcodes:\n\n- Intel Xeon E-2186G CPU with a power rating of 95W\n-Intel Xeon E-2176G CPU with a power rating of 80W\n-Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server opetechrae:\n\n- Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server test-emtech-rae-api:\n\n- Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W\n\nSuggestions for Volvo server ava-emtech-rae:\n\n- Intel Xeon E-2186G CPU with a power rating of 95W\n- Intel Xeon E-2176G CPU with a power rating of 80W\n- Intel Xeon E-2244G CPU with a power rating of 95W"}
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
          <Typography>
          {"\n\n1. Volvo server emtech-rae: Liquid cooling with estimated cost of around $500.\n2. Volvo server test-ava-rae/ETRAEdb: Air-cooled radiator with estimated cost of around $300.\n3. Volvo server test-ava-rae/ETRAEdbtest: Liquid cooling with estimated cost of around $400.\n4. Volvo server test-ava-rae/master: Air-cooled radiator with estimated cost of around $400.\n5. Volvo server test-ava-rae/RAEDb: Air-cooled radiator with estimated cost of around $300.\n6. Volvo server raeledgerstorage: Liquid cooling with estimated cost of around $600.\n7. Volvo server raeterraformcodes: Liquid cooling with estimated cost of around $700.\n8. Volvo server opetechrae: Air-cooled radiator with estimated cost of around $400.\n9. Volvo server test-emtech-rae-api: Air-cooled radiator with estimated cost of around $400.\n10. Volvo server ava-emtech-rae: Liquid cooling with estimated cost of around $500."}
          </Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default ResourceGroup;