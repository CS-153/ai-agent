import json
from typing import Dict, List

from mistralai import Any, Optional


class Recipe:
    def __init__(
        self,
        name: str,
        ingredients: Dict[str, Dict[str, str]],
        steps: List[str],
        prep_time: int,
        cook_time: int,
        servings: int,
        cuisine: str,
        summary: str,
        difficulty: str,
    ):
        """
        Initializes a Recipe object.
        :param name: str - Name of the recipe.
        :param ingredients: dict - Dictionary with ingredients as keys and values containing 'quantity' and 'unit'.
        :param steps: list of str - Ordered list of cooking steps.
        :param prep_time: int - Preparation time in minutes.
        :param cook_time: int - Cooking time in minutes.
        :param servings: int (optional) - Number of servings.
        :param cuisine: str (optional) - Type of cuisine.
        :param summary: str (optional) - Short description of the recipe.
        :param likes: int (optional) - Number of likes for the recipe.
        :param difficulty: str (optional) - Difficulty level of the recipe.
        """
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.cuisine = cuisine
        self.summary = summary
        self.difficulty = difficulty

    @property
    def total_time(self):
        """Returns the total time required for the recipe."""
        return self.prep_time + self.cook_time

    def to_json(self):
        """Serializes the Recipe object to JSON."""
        return json.dumps(
            {
                "name": self.name,
                "ingredients": self.ingredients,
                "steps": self.steps,
                "prep_time": self.prep_time,
                "cook_time": self.cook_time,
                "servings": self.servings,
                "cuisine": self.cuisine,
                "summary": self.summary,
                "difficulty": self.difficulty,
            }
        )

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        """Deserializes JSON into a Recipe object."""
        return cls(
            name=data["name"],
            ingredients=data["ingredients"],
            steps=data["steps"],
            prep_time=data["prep_time"],
            cook_time=data["cook_time"],
            servings=data.get("servings"),
            cuisine=data.get("cuisine"),
            summary=data.get("summary"),
            difficulty=data.get("difficulty"),
        )


class RecipeSummary:
    def __init__(self, recipe: Recipe):
        self.recipe = recipe

    @property
    def summary(self):
        return f"""# {self.recipe.name}:\n{self.recipe.cuisine} recipe that serves {self.recipe.servings} people. It takes {self.recipe.prep_time} minutes to prepare and {self.recipe.cook_time} minutes to cook. The total time is {self.recipe.total_time} minutes."""

    @property
    def ingredients(self):
        return f"Ingredients:\n{'\n'.join([
            f'- **{item}**: {details['quantity']} {details['unit']}' for item, details in self.recipe.ingredients.items()
        ])}"

    @property
    def steps(self):
        return f"Steps:\n{'\n'.join([f'{i}. {step}' for i, step in enumerate(self.recipe.steps, 1)])}"
