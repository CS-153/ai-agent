import { Box, Flex, Heading, IconButton } from "@chakra-ui/react";
import { FaHome, FaPlus } from "react-icons/fa";
import { Link } from "react-router-dom";

function AppBar() {
  return (
    <Box
      as="header"
      position="sticky"
      top="0"
      zIndex="100"
      bg="white"
      boxShadow="md"
      px={6}
      py={4}
    >
      <Flex align="center" justify="space-between" maxW="900px" mx="auto">
        {/* Left - Home Button */}
        <Link to="/">
          <IconButton
            aria-label="Home"
            size="lg"
            variant="ghost"
            color="green.500"
            _hover={{ bg: "gray.200" }}
          >
            <FaHome />
          </IconButton>
        </Link>

        {/* Center - App Title */}
        <Heading
          as="h1"
          size="lg"
          fontWeight="bold"
          textAlign="center"
          flex="1"
        >
          <Link to="/" style={{ textDecoration: "none", color: "inherit" }}>
            Tomaba
          </Link>
        </Heading>
        {/* Right - Create Button */}
        <Link to="/create">
          <IconButton
            aria-label="Create"
            size="lg"
            variant="ghost"
            color="green.500"
            _hover={{ bg: "gray.200" }}
          >
            <FaPlus />
          </IconButton>
        </Link>
      </Flex>
    </Box>
  );
}

export default AppBar;
