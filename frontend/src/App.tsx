import { useEffect, useState } from "react";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";

import Dashboard from "./pages/Dashboard";
import RubricManagement from "./pages/RubricManagement";
import ResourcesPage from "./pages/ResourcesPage";

const routes = [
  { path: "/", label: "Agenda", component: <Dashboard /> },
  { path: "/resources", label: "Resources", component: <ResourcesPage /> },
  { path: "/rubrics", label: "Rubrics", component: <RubricManagement /> }
];

export default function App() {
  const location = useLocation();
  const [tabIndex, setTabIndex] = useState(0);

  useEffect(() => {
    const index = routes.findIndex((route) => route.path === location.pathname);
    setTabIndex(index === -1 ? 0 : index);
  }, [location.pathname]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Agenda Planner
          </Typography>
          <Tabs value={tabIndex} textColor="inherit" indicatorColor="secondary">
            {routes.map((route) => (
              <Tab
                key={route.path}
                label={route.label}
                component={Link}
                to={route.path}
              />
            ))}
          </Tabs>
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ p: 3 }}>
        <Routes>
          {routes.map((route) => (
            <Route key={route.path} path={route.path} element={route.component} />
          ))}
        </Routes>
      </Box>
    </Box>
  );
}
