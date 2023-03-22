import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./scenes/global/Sidebar";
import Topbar from "./scenes/global/Topbar";
import Footer from "./scenes/global/Footer";
import PastUsage from "./scenes/pastUsage";
import FuturePred from "./scenes/futurePred";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "./theme";
import ResourceGroup from "./scenes/resourceGroup";
import Region from "./scenes/region";
import Home from "./scenes/home";


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
                  <Route path="/" element={<Home />} />
                  <Route path="/pastUsage" element={<PastUsage />} />
                  <Route path="/futurePred" element={<FuturePred />} />
                  <Route path="/resourceGroup" element={<ResourceGroup />} />
                  <Route path="/region" element={<Region />} />
                </Routes>
              <Footer setIsSidebar={setIsSidebar} />
            </main>
          </div>    
        </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
