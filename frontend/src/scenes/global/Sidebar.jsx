import { useState } from "react";
import { ProSidebar, Menu, MenuItem } from "react-pro-sidebar";
import { Box, IconButton, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";
import "react-pro-sidebar/dist/css/styles.css";
import { tokens } from "../../theme";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import HistoryIcon from '@mui/icons-material/History';
import UpdateIcon from '@mui/icons-material/Update';
import StorageIcon from '@mui/icons-material/Storage';
import SouthAmericaIcon from '@mui/icons-material/SouthAmerica';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";

const Item = ({ title, to, icon, selected, setSelected }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <MenuItem
      active={selected === title}
      style={{
        color: colors.grey[100],
      }}
      onClick={() => setSelected(title)}
      icon={icon}
    >
      <Typography>{title}</Typography>
      <Link to={to} />
    </MenuItem>
  );
};

const Sidebar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [selected, setSelected] = useState("Dashboard");

  return (
    <Box
      sx={{
        "& .pro-sidebar-inner": {
          background: `${colors.primary[400]} !important`,
        },
        "& .pro-icon-wrapper": {
          backgroundColor: "transparent !important",
        },
        "& .pro-inner-item": {
          padding: "5px 35px 5px 20px !important",
        },
        "& .pro-inner-item:hover": {
          color: "#868dfb !important",
        },
        "& .pro-menu-item.active": {
          color: "#6870fa !important",
        },
      }}
    >
      <ProSidebar collapsed={isCollapsed}  style={{ height: "1200px" }}>
        <Menu iconShape="square">
          {/* LOGO AND MENU ICON */}
          <MenuItem
            onClick={() => setIsCollapsed(!isCollapsed)}
            icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
            style={{
              margin: "10px 0 20px 0",
              color: colors.grey[100],
            }}
          >
            
            {!isCollapsed && (
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                right="75px"
              >
                <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                  <MenuOutlinedIcon />
                </IconButton>
              </Box>
            )}
          </MenuItem>

          {!isCollapsed && (
            <Box mb="25px">
              <Box display="flex" justifyContent="center" alignItems="center">

              {theme.palette.mode === "dark" ? (
                    <img
                    alt="Volvo Logo"
                    width="150px"
                    height="150px"
                    src={`../../assets/VolvoDark.png`}
                  />
                  ) : (
                    <img
                    alt="Volvo Logo"
                    width="150px"
                    height="150px"
                    src={`../../assets/VolvoLight.png`}
                  />
                  )}

                
              </Box>
              <Box textAlign="center">
                
                <Typography variant="h5" color={colors.greenAccent[500]} marginTop="20px">
                  Carbon Analysis Dashboard
                </Typography>
              </Box>
            </Box>
          )}


          <Box paddingLeft={isCollapsed ? undefined : "10%"}>
            <Item
                title="Home"
                to="/"
                icon={<HomeOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

            <Typography
              variant="h6"
              color={colors.grey[300]}
              sx={{ m: "15px 0 5px 20px" }}
            >
              Data
            </Typography>
            <Item
              title="Past Usage"
              to="/pastUsage"
              icon={<HistoryIcon/>} 
              selected={selected}
              setSelected={setSelected}
            />
            <Item
              title="Future Prediction"
              to="/futurePred"
              icon={<UpdateIcon />}
              selected={selected}
              setSelected={setSelected}
            />

            <Typography
              variant="h6"
              color={colors.grey[300]}
              sx={{ m: "15px 0 5px 20px" }}
            >

            Future Advice
            </Typography>
            <Item
              title="Resource Group"
              to="/resourceGroup"
              icon={<StorageIcon />}
              selected={selected}
              setSelected={setSelected}
            />
            <Item
              title="Region"
              to="/region"
              icon={<SouthAmericaIcon />}
              selected={selected}
              setSelected={setSelected}
            />
          </Box>
        </Menu>
      </ProSidebar>
    </Box>
  );
};

export default Sidebar;
