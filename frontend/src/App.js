import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./scenes/global/Sidebar";
import Topbar from "./scenes/global/Topbar";
import PastUsage from "./scenes/pastUsage";
import FuturePred from "./scenes/futurePred";
import RealTime from "./scenes/realTime";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "./theme";
import ResourceGroup from "./scenes/resourceGroup";
import Region from "./scenes/region";
import Welcome from "./scenes/welcome";


function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <Sidebar isSidebar={isSidebar} />
          <main className="content">
          <Topbar setIsSidebar={setIsSidebar} />
            <Routes>
              <Route path="/welcome" element={<Welcome />} />
              <Route path="/pastUsage" element={<PastUsage />} />
              <Route path="/realTime" element={<RealTime />} />
              <Route path="/futurePred" element={<FuturePred />} />
              <Route path="/resourceGroup" element={<ResourceGroup />} />
              <Route path="/region" element={<Region />} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
