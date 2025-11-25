"""
Recipe Quantity Adjuster
Scales ingredient amounts based on desired servings
Original recipe serves 12 people
"""

# ============================================================================
# CONSTANTS
# ============================================================================
ORIGINAL_SERVINGS = 12
MIN_SERVINGS = 1
MAX_SERVINGS = 100

# Original recipe ingredients (for 12 servings)
ORIGINAL_RECIPE = {
    "flour": {"amount": 3, "unit": "cups"},
    "sugar": {"amount": 2, "unit": "cups"},
    "butter": {"amount": 1, "unit": "cup"},
    "eggs": {"amount": 4, "unit": "large"},
    "milk": {"amount": 1.5, "unit": "cups"},
    "baking_powder": {"amount": 2, "unit": "teaspoons"},
    "vanilla_extract": {"amount": 1, "unit": "teaspoon"},
    "salt": {"amount": 0.5, "unit": "teaspoon"}
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_ingredient_name(ingredient: str) -> str:
    """Convert ingredient key to readable name."""
    return ingredient.replace("_", " ").title()


def format_amount(amount: float) -> str:
    """
    Format amount for display, converting to fractions when appropriate.
    
    Edge Cases:
        - Whole numbers (2.0 -> "2")
        - Common fractions (0.5 -> "1/2", 0.25 -> "1/4", 0.75 -> "3/4")
        - Mixed numbers (1.5 -> "1 1/2")
        - Decimals for uncommon fractions
    """
    # Precondition: amount must be a positive number
    assert isinstance(amount, (int, float)), f"Amount must be numeric, got {type(amount)}"
    assert amount > 0, f"Amount must be positive, got {amount}"
    
    # Check if it's a whole number
    if amount == int(amount):
        return str(int(amount))
    
    # Common fraction mappings (strict matching to avoid 0.33 != 1/3)
    fractions = {
        0.25: "1/4",
        0.5: "1/2",
        0.75: "3/4"
    }
    
    # Check for whole number + fraction
    whole = int(amount)
    decimal = round(amount - whole, 2)
    
    if whole > 0 and decimal in fractions:
        return f"{whole} {fractions[decimal]}"
    elif decimal in fractions:
        return fractions[decimal]
    
    # Round to 2 decimal places for other values
    return f"{amount:.2f}".rstrip('0').rstrip('.')


def is_valid_servings(servings_str: str) -> tuple[bool, str, int]:
    """
    Validate servings input.
    
    Args:
        servings_str: String input from user
        
    Returns:
        Tuple of (is_valid, error_message, parsed_value)
        
    Edge Cases:
        - Empty string
        - Non-numeric input
        - Zero or negative values
        - Extremely large values
        - Decimal values
    """
    # Input type check
    assert isinstance(servings_str, str), f"Input must be string, got {type(servings_str)}"
    
    if not servings_str:
        return False, "Servings cannot be empty", 0
    
    servings_str = servings_str.strip()
    
    try:
        servings = float(servings_str)
        
        # Check if it's effectively an integer
        if servings != int(servings):
            return False, "Servings must be a whole number", 0
        
        servings = int(servings)
        
    except ValueError:
        return False, "Servings must be a valid number", 0
    
    if servings < MIN_SERVINGS:
        return False, f"Servings must be at least {MIN_SERVINGS}", 0
    
    if servings > MAX_SERVINGS:
        return False, f"Servings cannot exceed {MAX_SERVINGS}", 0
    
    # Postcondition: result should be valid
    assert MIN_SERVINGS <= servings <= MAX_SERVINGS, f"Internal error: validated value out of range"
    
    return True, "", servings


def calculate_scaling_factor(original: int, desired: int) -> float:
    """
    Calculate the scaling factor for recipe adjustment.
    
    Args:
        original: Original number of servings
        desired: Desired number of servings
        
    Returns:
        Scaling factor (multiplier)
    """
    # Preconditions
    assert isinstance(original, int), f"Original servings must be int, got {type(original)}"
    assert isinstance(desired, int), f"Desired servings must be int, got {type(desired)}"
    assert original > 0, f"Original servings must be positive, got {original}"
    assert desired > 0, f"Desired servings must be positive, got {desired}"
    
    result = desired / original
    
    # Postcondition: result should be positive
    assert result > 0, f"Scaling factor should be positive, got {result}"
    # Postcondition: result should be reasonable (not extreme)
    assert result <= 100, f"Scaling factor too large: {result}. Check inputs."
    
    return result


def scale_recipe(recipe: dict, scaling_factor: float) -> dict:
    """
    Scale all ingredients in the recipe by the scaling factor.
    
    Args:
        recipe: Dictionary of ingredients with amounts and units
        scaling_factor: Multiplier for scaling
        
    Returns:
        New dictionary with scaled amounts
    """
    # Preconditions
    assert isinstance(recipe, dict), f"Recipe must be dict, got {type(recipe)}"
    assert len(recipe) > 0, "Recipe cannot be empty"
    assert isinstance(scaling_factor, (int, float)), f"Scaling factor must be numeric, got {type(scaling_factor)}"
    assert scaling_factor > 0, f"Scaling factor must be positive, got {scaling_factor}"
    
    # Validate recipe structure
    for ingredient, details in recipe.items():
        assert isinstance(details, dict), f"Recipe item '{ingredient}' must be dict, got {type(details)}"
        assert "amount" in details, f"Recipe item '{ingredient}' missing 'amount' key"
        assert "unit" in details, f"Recipe item '{ingredient}' missing 'unit' key"
        assert isinstance(details["amount"], (int, float)), f"Amount for '{ingredient}' must be numeric"
        assert details["amount"] > 0, f"Amount for '{ingredient}' must be positive, got {details['amount']}"
        assert isinstance(details["unit"], str), f"Unit for '{ingredient}' must be string"
    
    scaled_recipe = {}
    
    for ingredient, details in recipe.items():
        scaled_amount = details["amount"] * scaling_factor
        # Sanity check: scaled amounts should remain reasonable
        assert scaled_amount > 0, f"Scaled amount for '{ingredient}' is not positive"
        assert scaled_amount < 10000, f"Scaled amount for '{ingredient}' seems unreasonably large: {scaled_amount}"
        
        scaled_recipe[ingredient] = {
            "amount": scaled_amount,
            "unit": details["unit"]
        }
    
    # Postcondition: scaled recipe should have same keys as original
    assert set(scaled_recipe.keys()) == set(recipe.keys()), "Scaled recipe has different keys than original"
    assert len(scaled_recipe) == len(recipe), "Scaled recipe size mismatch"
    
    return scaled_recipe


def display_recipe(recipe: dict, servings: int):
    """
    Display the recipe in a formatted, readable way.
    
    Args:
        recipe: Dictionary of ingredients
        servings: Number of servings this recipe makes
    """
    # Preconditions
    assert isinstance(recipe, dict), f"Recipe must be dict, got {type(recipe)}"
    assert len(recipe) > 0, "Recipe cannot be empty"
    assert isinstance(servings, int), f"Servings must be int, got {type(servings)}"
    assert servings > 0, f"Servings must be positive, got {servings}"
    assert MIN_SERVINGS <= servings <= MAX_SERVINGS, f"Servings {servings} out of valid range [{MIN_SERVINGS}, {MAX_SERVINGS}]"
    
    print(f"\n{'='*60}")
    print(f"RECIPE FOR {servings} SERVINGS")
    print(f"{'='*60}\n")
    
    print("INGREDIENTS:")
    print("-" * 60)
    
    for ingredient, details in recipe.items():
        name = format_ingredient_name(ingredient)
        amount = format_amount(details["amount"])
        unit = details["unit"]
        print(f"  • {amount:>8} {unit:<12} {name}")
    
    print("-" * 60)


def compare_recipes(original: dict, scaled: dict, original_servings: int, new_servings: int):
    """
    Show side-by-side comparison of original and scaled recipes.
    
    Args:
        original: Original recipe dictionary
        scaled: Scaled recipe dictionary
        original_servings: Original serving count
        new_servings: New serving count
    """
    # Preconditions
    assert isinstance(original, dict), f"Original recipe must be dict, got {type(original)}"
    assert isinstance(scaled, dict), f"Scaled recipe must be dict, got {type(scaled)}"
    assert len(original) > 0, "Original recipe cannot be empty"
    assert len(scaled) > 0, "Scaled recipe cannot be empty"
    assert isinstance(original_servings, int), f"Original servings must be int, got {type(original_servings)}"
    assert isinstance(new_servings, int), f"New servings must be int, got {type(new_servings)}"
    assert original_servings > 0, f"Original servings must be positive, got {original_servings}"
    assert new_servings > 0, f"New servings must be positive, got {new_servings}"
    assert set(original.keys()) == set(scaled.keys()), "Original and scaled recipes have different ingredients"
    
    print(f"\n{'='*70}")
    print(f"RECIPE COMPARISON")
    print(f"{'='*70}")
    print(f"{'INGREDIENT':<20} {'ORIGINAL ('+str(original_servings)+')':>20} {'NEW ('+str(new_servings)+')':>20}")
    print("-" * 70)
    
    for ingredient in original.keys():
        name = format_ingredient_name(ingredient)
        
        orig_amount = format_amount(original[ingredient]["amount"])
        orig_unit = original[ingredient]["unit"]
        orig_str = f"{orig_amount} {orig_unit}"
        
        new_amount = format_amount(scaled[ingredient]["amount"])
        new_unit = scaled[ingredient]["unit"]
        new_str = f"{new_amount} {new_unit}"
        
        print(f"{name:<20} {orig_str:>20} {new_str:>20}")
    
    print("-" * 70)


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def recipe_adjuster():
    """
    Main program to adjust recipe quantities based on desired servings.
    Handles input validation and displays results.
    """
    # Validate constants and ORIGINAL_RECIPE structure at startup
    assert isinstance(ORIGINAL_SERVINGS, int), "ORIGINAL_SERVINGS must be int"
    assert ORIGINAL_SERVINGS > 0, "ORIGINAL_SERVINGS must be positive"
    assert isinstance(MIN_SERVINGS, int) and MIN_SERVINGS > 0, "MIN_SERVINGS must be positive int"
    assert isinstance(MAX_SERVINGS, int) and MAX_SERVINGS > MIN_SERVINGS, "MAX_SERVINGS must be > MIN_SERVINGS"
    assert ORIGINAL_SERVINGS >= MIN_SERVINGS and ORIGINAL_SERVINGS <= MAX_SERVINGS, "ORIGINAL_SERVINGS out of valid range"
    assert isinstance(ORIGINAL_RECIPE, dict), "ORIGINAL_RECIPE must be dict"
    assert len(ORIGINAL_RECIPE) > 0, "ORIGINAL_RECIPE cannot be empty"
    
    print("\n" + "="*70)
    print("🍰  RECIPE QUANTITY ADJUSTER")
    print("="*70)
    print(f"Original recipe serves: {ORIGINAL_SERVINGS} people")
    print("="*70)
    
    try:
        while True:
            # Get desired servings with validation
            servings_input = input(f"\nHow many servings do you need? ({MIN_SERVINGS}-{MAX_SERVINGS}): ").strip()
            
            is_valid, error_msg, desired_servings = is_valid_servings(servings_input)
            
            if not is_valid:
                print(f"❌ {error_msg}")
                continue
            
            # Calculate scaling factor
            scaling_factor = calculate_scaling_factor(ORIGINAL_SERVINGS, desired_servings)
            
            print(f"\n📊 Scaling factor: {scaling_factor:.2f}x")
            
            if scaling_factor == 1.0:
                print("✅ No scaling needed! Use the original recipe.")
                display_recipe(ORIGINAL_RECIPE, ORIGINAL_SERVINGS)
            else:
                # Scale the recipe
                scaled_recipe = scale_recipe(ORIGINAL_RECIPE, scaling_factor)
                
                # Display scaled recipe
                display_recipe(scaled_recipe, desired_servings)
                
                # Ask if user wants to see comparison
                show_comparison = input("\nShow comparison with original recipe? (y/n): ").strip().lower()
                
                if show_comparison in ['y', 'yes']:
                    compare_recipes(ORIGINAL_RECIPE, scaled_recipe, ORIGINAL_SERVINGS, desired_servings)
            
            # Ask if user wants to scale for different servings
            another = input("\n\nScale for different number of servings? (y/n): ").strip().lower()
            
            if another not in ['y', 'yes']:
                print("\n👨‍🍳 Happy cooking! Enjoy your recipe!")
                break
    
    except EOFError:
        print("\n\n⚠️  Input interrupted. Exiting program.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user. Exiting.")


# ============================================================================
# UNIT TESTS
# ============================================================================

def run_tests():
    """Test validation and calculation functions."""
    print("\n🧪 RUNNING UNIT TESTS...\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test is_valid_servings
    print("Testing is_valid_servings():")
    test_cases = [
        ("12", True, "Valid standard number"),
        ("1", True, "Minimum servings"),
        ("100", True, "Maximum servings"),
        ("0", False, "Zero servings"),
        ("-5", False, "Negative servings"),
        ("", False, "Empty string"),
        ("abc", False, "Non-numeric"),
        ("12.5", False, "Decimal number"),
        ("150", False, "Exceeds maximum"),
        ("  24  ", True, "With whitespace"),
    ]
    
    for servings, expected_valid, description in test_cases:
        is_valid, _, result_val = is_valid_servings(servings)
        status = "✅" if is_valid == expected_valid else "❌"
        if is_valid == expected_valid:
            tests_passed += 1
        else:
            tests_failed += 1
        print(f"  {status} {description}: '{servings}' -> {is_valid}")
        # Additional assertion on successful parse
        if is_valid:
            assert isinstance(result_val, int), f"Parsed value should be int, got {type(result_val)}"
            assert MIN_SERVINGS <= result_val <= MAX_SERVINGS, f"Parsed value {result_val} out of valid range"
    
    # Test calculate_scaling_factor
    print("\nTesting calculate_scaling_factor():")
    test_cases_scaling = [
        (12, 12, 1.0, "Same servings"),
        (12, 24, 2.0, "Double servings"),
        (12, 6, 0.5, "Half servings"),
        (12, 36, 3.0, "Triple servings"),
        (12, 1, 0.083, "Single serving"),
    ]
    
    for orig, desired, expected, description in test_cases_scaling:
        result = calculate_scaling_factor(orig, desired)
        status = "✅" if abs(result - expected) < 0.01 else "❌"
        if abs(result - expected) < 0.01:
            tests_passed += 1
        else:
            tests_failed += 1
        print(f"  {status} {description}: {orig} -> {desired} = {result:.2f}x")
        # Assertion: result should be positive and reasonable
        assert result > 0, f"Scaling factor should be positive"
        assert result <= 100, f"Scaling factor {result} seems unreasonably large"
    
    # Test format_amount
    print("\nTesting format_amount():")
    test_cases_format = [
        (1.0, "1", "Whole number"),
        (0.5, "1/2", "Half"),
        (0.25, "1/4", "Quarter"),
        (0.75, "3/4", "Three quarters"),
        (1.5, "1 1/2", "One and a half"),
        (2.33, "2.33", "Uncommon decimal"),
    ]
    
    for amount, expected, description in test_cases_format:
        result = format_amount(amount)
        status = "✅" if result == expected else "❌"
        if result == expected:
            tests_passed += 1
        else:
            tests_failed += 1
        print(f"  {status} {description}: {amount} -> '{result}'")
        # Assertion: result should be non-empty string
        assert isinstance(result, str), f"format_amount should return string, got {type(result)}"
        assert len(result) > 0, f"format_amount returned empty string"
    
    # Test scale_recipe
    print("\nTesting scale_recipe():")
    test_recipe = {
        "ingredient1": {"amount": 2.0, "unit": "cups"},
        "ingredient2": {"amount": 1.0, "unit": "tbsp"}
    }
    scaled = scale_recipe(test_recipe, 2.0)
    assert len(scaled) == len(test_recipe), "Scaled recipe should have same number of ingredients"
    assert scaled["ingredient1"]["amount"] == 4.0, "Scaling by 2.0 should double amounts"
    assert scaled["ingredient1"]["unit"] == "cups", "Units should be preserved"
    tests_passed += 1
    print(f"  ✅ Scale recipe by 2.0x: amounts doubled correctly")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"TESTS COMPLETED")
    print(f"Passed: {tests_passed} | Failed: {tests_failed}")
    if tests_failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {tests_failed} test(s) failed")
    print(f"{'='*50}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Uncomment to run tests first
    run_tests()
    
    # Start the recipe adjuster
    recipe_adjuster()

    