import {
  Badge,
  Box,
  Heading,
  HStack,
  IconButton,
  Image,
  Text,
} from "@chakra-ui/react";
import { useState } from "react";
import { Helmet } from "react-helmet-async";

import { FaHeart } from "react-icons/fa";
import { PiCookingPotFill, PiKnifeFill } from "react-icons/pi";

interface RecipeCardProps {
  id: string;
  name: string;
  summary: string;
  difficulty: "Easy" | "Medium" | "Hard";
  prep_time: number;
  cook_time: number;
  imageUrl?: string;
}

export function RecipeCard({
  name,
  summary,
  difficulty,
  prep_time,
  cook_time,
  id,
}: RecipeCardProps) {
  const [liked, setLiked] = useState(false);

  const difficultyColors = {
    Easy: "green",
    Medium: "orange",
    Hard: "red",
  };
  const imageUrl = `https://storage.googleapis.com/tomaba-recipes/images/${id}.jpg`;

  return (
    <>
      {/* Open Graph Meta Tags */}
      <Helmet>
        <title>Tomaba - Recipe</title>
        <meta property="og:title" content="Tomaba - AI Recipe Agent" />
        <meta
          property="og:description"
          content="Discover and create personalized AI-powered recipes!"
        />
        <meta property="og:image" content={imageUrl} />
        <meta
          property="og:url"
          content={`http://localhost:5173/recipe/${id}`}
        />
        <meta property="og:type" content="website" />

        {/* Twitter Card for iOS/iMessage */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Tomaba - AI Recipe Agent" />
        <meta
          name="twitter:description"
          content="Explore and create AI-powered recipes!"
        />
        <meta name="twitter:image" content={imageUrl} />
      </Helmet>
      <Box
        p={5}
        borderRadius="lg"
        boxShadow="md"
        bg="white"
        transition="transform 0.2s ease-in-out"
        _hover={{ transform: "scale(1.03)", boxShadow: "lg" }}
        position="relative"
        display="flex"
        flexDirection="column"
        gap={2}
      >
        {/* Recipe Image */}
        {imageUrl && (
          <Image
            src={imageUrl}
            alt={name}
            borderRadius="md"
            w="100%"
            h="150px"
            objectFit="cover"
            mb={3}
          />
        )}

        {/* Difficulty Badge */}
        <Badge
          bg={`${difficultyColors[difficulty]}.100`}
          color={`${difficultyColors[difficulty]}.700`}
          position="absolute"
          top={2}
          left={2}
          px={3}
          py={1}
          fontSize="xs"
          fontWeight="bold"
          borderRadius="md"
          boxShadow="sm"
        >
          {difficulty}
        </Badge>

        {/* Recipe Name */}
        <Heading as="h3" size="md" mb={1}>
          {name}
        </Heading>

        {/* Summary */}
        <Text fontSize="sm" color="gray.600">
          {summary || "No summary available"}
        </Text>

        {/* Prep & Cook Time */}
        <HStack mt={3} gap={4} fontSize="sm" color="gray.700">
          <HStack>
            <PiKnifeFill />
            <Text>{prep_time} min</Text>
          </HStack>
          <HStack>
            <PiCookingPotFill />
            <Text>{cook_time} min</Text>
          </HStack>
        </HStack>

        {/* Like Button */}
        <IconButton
          aria-label="Like recipe"
          size="sm"
          colorScheme={liked ? "red" : "gray"}
          variant="ghost"
          position="absolute"
          bottom={2}
          right={2}
          onClick={(e) => {
            e.preventDefault();
            setLiked(!liked);
          }}
        >
          <FaHeart />
        </IconButton>
      </Box>
    </>
  );
}
