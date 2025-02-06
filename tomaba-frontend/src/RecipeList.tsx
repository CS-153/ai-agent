import { Grid, Heading, Spinner, Text, VStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { RecipeCard } from "./RecipeCard"; // Import new RecipeCard component

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface Recipe {
  id: string;
  name: string;
  summary: string;
  difficulty: "Easy" | "Medium" | "Hard";
  prep_time: number;
  cook_time: number;
}

function RecipeList() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/recipes`)
      .then((res) => res.json())
      .then((data: Recipe[]) => {
        setRecipes(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <Spinner size="xl" mt={10} />;
  if (error)
    return (
      <Text color="red.500" mt={4}>
        {error}
      </Text>
    );
  if (recipes.length === 0) return <Text mt={4}>No recipes found.</Text>;

  return (
    <VStack gap={6} align="start" w="100%">
      <Heading as="h2" size="xl" fontWeight="bold">
        Discover Recipes
      </Heading>

      <Grid
        templateColumns={{ base: "1fr", md: "repeat(2, 1fr)" }}
        gap={6}
        w="100%"
      >
        {recipes.map((recipe) => (
          <RouterLink
            key={recipe.id}
            to={`/recipe/${recipe.id}`}
            style={{ textDecoration: "none" }}
          >
            <RecipeCard {...recipe} />
          </RouterLink>
        ))}
      </Grid>
    </VStack>
  );
}

export default RecipeList;
