import {
  Box,
  Flex,
  Heading,
  SimpleGrid,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface Ingredient {
  quantity: string;
  unit: string;
}

interface Recipe {
  name: string;
  summary: string;
  cuisine: string;
  difficulty: string;
  prep_time: number;
  cook_time: number;
  servings: number;
  ingredients: Record<string, Ingredient>;
  steps: string[];
}

function RecipePage() {
  const { id } = useParams<{ id: string }>();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/recipe/${id}`)
      .then((res) => res.json())
      .then((data: Recipe) => {
        setRecipe(data);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <Spinner size="xl" mt={10} />;
  if (error)
    return (
      <Text color="red.500" mt={4}>
        {error}
      </Text>
    );
  if (!recipe) return null;

  return (
    <Box
      maxW="800px"
      mx="auto"
      p={6}
      bg="white"
      boxShadow="lg"
      borderRadius="lg"
    >
      {/* Recipe Name */}
      <Heading as="h2" size="xl" mb={4} textAlign="center">
        {recipe.name}
      </Heading>

      {/* Recipe Summary */}
      <Text
        fontSize="lg"
        fontStyle="italic"
        textAlign="center"
        mb={6}
        color="gray.600"
      >
        {recipe.summary}
      </Text>

      {/* Recipe Info Grid */}
      <SimpleGrid columns={2} gap={6} mb={6}>
        <Text>
          <strong>Cuisine:</strong> {recipe.cuisine}
        </Text>
        <Text>
          <strong>Difficulty:</strong> {recipe.difficulty}
        </Text>
        <Text>
          <strong>Prep Time:</strong> {recipe.prep_time} mins
        </Text>
        <Text>
          <strong>Cook Time:</strong> {recipe.cook_time} mins
        </Text>
        <Text>
          <strong>Servings:</strong> {recipe.servings}
        </Text>
      </SimpleGrid>

      {/* <Divider my={6} /> */}

      {/* Ingredients Section */}
      <Box mb={6}>
        <Heading as="h3" size="md" mb={3}>
          Ingredients
        </Heading>
        <VStack align="start" gap={2}>
          {Object.entries(recipe.ingredients).map(([name, details]) => (
            <Flex
              key={name}
              w="100%"
              justify="space-between"
              bg="gray.50"
              p={3}
              borderRadius="md"
            >
              <Text fontWeight="medium">{name}</Text>
              <Text>
                {details.quantity} {details.unit}
              </Text>
            </Flex>
          ))}
        </VStack>
      </Box>

      {/* <Divider my={6} /> */}

      {/* Steps Section */}
      <Box>
        <Heading as="h3" size="md" mb={3}>
          Instructions
        </Heading>
        <VStack gap={4} align="stretch">
          {recipe.steps.map((step, index) => (
            <Box
              key={index}
              bg="gray.50"
              boxShadow="sm"
              p={4}
              borderRadius="md"
            >
              <Text>
                <strong>Step {index + 1}:</strong> {step}
              </Text>
            </Box>
          ))}
        </VStack>
      </Box>
    </Box>
  );
}

export default RecipePage;
