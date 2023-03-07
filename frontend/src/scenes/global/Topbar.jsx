import { Box, IconButton, useTheme } from "@mui/material";
import { useContext } from "react";
import { ColorModeContext, tokens } from "../../theme";
import InputBase from "@mui/material/InputBase";
import SearchIcon from "@mui/icons-material/Search";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";

const Topbar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);

  return (
    <Box display="flex" justifyContent="space-between">
      <Box position="absolute" right="0px"  p={2}>
        {/* ICONS */}
        <IconButton onClick={colorMode.toggleColorMode}>
          {theme.palette.mode === "dark" ? (
            <DarkModeOutlinedIcon />
          ) : (
            <LightModeOutlinedIcon />
          )}
        </IconButton>
      </Box>

      {/* SEARCH BAR */}
      <Box
      backgroundColor={colors.primary[400]}
      borderRadius="3px"
      position="absolute"
      left="60%"
      top="20px"
      >
    
      <InputBase sx={{ ml: 2, flex: 1 }} placeholder="Enter Region" />
      <IconButton type="button" sx={{ p: 2}}>
        <SearchIcon />
      </IconButton>
    </Box>
  </Box>
  );
};

export default Topbar;