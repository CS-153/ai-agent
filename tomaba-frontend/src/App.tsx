import { Box } from "@chakra-ui/react";
import { HelmetProvider } from "react-helmet-async";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AppBar from "./AppBar.tsx";
import CreatePage from "./CreatePage.tsx";
import RecipeList from "./RecipeList.tsx";
import RecipePage from "./RecipePage.tsx";

function App() {
  return (
    <HelmetProvider>
      <Router>
        <Box minH="100vh" bg="gray.50">
          {/* Add the App Bar */}
          <AppBar />

          {/* Page Content */}
          <Box maxW="800px" mx="auto" p={6}>
            <Routes>
              <Route path="/" element={<RecipeList />} />
              <Route path="/recipe/:id" element={<RecipePage />} />
              <Route path="/create" element={<CreatePage />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </HelmetProvider>
  );
}

export default App;
