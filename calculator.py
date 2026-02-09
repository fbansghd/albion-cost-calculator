"""
Calculator module for Albion Cost Calculator
Contains functions for recipe generation, cost calculation, and item list generation
"""

from config import material_prices, base_recipes, return_rate


def get_recipe_for_item(item_id):
    """
    Generate a recipe for a specific item based on its ID.

    Args:
        item_id (str): Item ID in format "T{tier}_{item_name}[@{enchant}]"
                      Example: "T5_MAIN_SWORD@1"

    Returns:
        dict: Recipe dictionary with material IDs and quantities
              Example: {"T5_BAR@1": 16, "T5_LEATHER@1": 8}
        None: If recipe cannot be generated
    """
    parts = item_id.split("_", 1)
    if len(parts) != 2:
        return None

    tier, item_part = parts

    # Extract enchantment level
    if "@" in item_part:
        base_item, enchant_str = item_part.split("@", 1)
        enchant = f"@{enchant_str}"
    else:
        base_item = item_part
        enchant = ""

    # Check if base recipe exists
    if base_item not in base_recipes:
        return None

    # Generate tier-specific recipe with enchantment
    base_recipe = base_recipes[base_item]
    recipe = {f"{tier}_{mat}{enchant}": qty for mat, qty in base_recipe.items()}

    return recipe


def calculate_cost(item_id):
    """
    Calculate the crafting cost of an item after accounting for resource return rate.

    Args:
        item_id (str): Item ID in format "T{tier}_{item_name}[@{enchant}]"

    Returns:
        float: Total cost after return rate adjustment
        None: If cost cannot be calculated (missing recipe or material prices)
    """
    recipe = get_recipe_for_item(item_id)
    if not recipe:
        return None

    total_cost = 0
    for mat, qty in recipe.items():
        if mat in material_prices:
            total_cost += material_prices[mat] * qty
        else:
            # Cannot calculate if any material price is missing
            return None

    # Apply return rate (resources returned from failed crafting attempts)
    return total_cost * (1 - return_rate)


def generate_all_items(item_names, tiers, enchant):
    """
    Generate a list of all item IDs from base names, tiers, and enchantment levels.

    Args:
        item_names (list): List of base item names (e.g., ["MAIN_SWORD", "OFF_SHIELD"])
        tiers (list): List of tier strings (e.g., ["T5", "T6", "T7"])
        enchant (list): List of enchantment strings (e.g., ["", "@1", "@2"])

    Returns:
        list: List of complete item IDs
              Example: ["T5_MAIN_SWORD", "T5_MAIN_SWORD@1", "T5_MAIN_SWORD@2", ...]
    """
    return [f"{tier}_{name}{q}" for name in item_names for tier in tiers for q in enchant]
