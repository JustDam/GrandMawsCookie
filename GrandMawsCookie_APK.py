"""
Recipe Quantity Adjuster - Mobile/APK Version
Scales ingredient amounts based on desired servings
Original recipe serves 12 people
Compatible with Kivy for Android APK deployment
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Set minimum window size for mobile screens (mobile-first)
Window.size = (400, 800)

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
# HELPER FUNCTIONS (Logic Layer - Unchanged)
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


def is_valid_servings(servings_str: str) -> tuple:
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


# ============================================================================
# KIVY UI APPLICATION
# ============================================================================

class RecipeAdjusterApp(App):
    """Mobile-friendly Recipe Adjuster Application using Kivy"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Recipe Adjuster"
        self.scaled_recipe = None
        self.desired_servings = 0
        
    def build(self):
        """Build the main UI layout"""
        # Validate startup conditions
        assert isinstance(ORIGINAL_SERVINGS, int), "ORIGINAL_SERVINGS must be int"
        assert ORIGINAL_SERVINGS > 0, "ORIGINAL_SERVINGS must be positive"
        assert isinstance(ORIGINAL_RECIPE, dict), "ORIGINAL_RECIPE must be dict"
        assert len(ORIGINAL_RECIPE) > 0, "ORIGINAL_RECIPE cannot be empty"
        
        # Main container - responsive to screen size
        main_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        # Header
        header = Label(
            text='[b]Grand Maws Cookie Recipe[/b]\n[size=14sp]Original: 12 servings[/size]',
            markup=True,
            size_hint_y=0.12,
            font_size='20sp'
        )
        main_layout.add_widget(header)
        
        # Input section
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing='5dp')
        
        input_label = Label(
            text='How many servings?',
            size_hint_y=0.4,
            font_size='14sp'
        )
        input_layout.add_widget(input_label)
        
        self.servings_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text=f'{MIN_SERVINGS}-{MAX_SERVINGS}',
            size_hint_y=0.6,
            font_size='16sp'
        )
        input_layout.add_widget(self.servings_input)
        main_layout.add_widget(input_layout)
        
        # Button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing='10dp')
        
        scale_btn = Button(
            text='Scale Recipe',
            size_hint_x=0.5,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        scale_btn.bind(on_press=self.on_scale_pressed)
        button_layout.add_widget(scale_btn)
        
        reset_btn = Button(
            text='Reset',
            size_hint_x=0.5,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        reset_btn.bind(on_press=self.on_reset_pressed)
        button_layout.add_widget(reset_btn)
        
        main_layout.add_widget(button_layout)
        
        # Results section - scrollable for mobile
        self.results_label = Label(
            text='Enter servings and tap Scale Recipe',
            markup=True,
            size_hint_y=0.63
        )
        
        scroll = ScrollView(size_hint_y=0.63)
        scroll.add_widget(self.results_label)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def on_scale_pressed(self, instance):
        """Handle scale recipe button press"""
        servings_str = self.servings_input.text.strip()
        
        is_valid, error_msg, desired_servings = is_valid_servings(servings_str)
        
        if not is_valid:
            self.show_error(error_msg)
            return
        
        # Calculate and display
        self.desired_servings = desired_servings
        scaling_factor = calculate_scaling_factor(ORIGINAL_SERVINGS, desired_servings)
        
        if scaling_factor == 1.0:
            self.display_original_recipe()
        else:
            self.scaled_recipe = scale_recipe(ORIGINAL_RECIPE, scaling_factor)
            self.display_scaled_recipe(self.scaled_recipe, desired_servings, scaling_factor)
    
    def on_reset_pressed(self, instance):
        """Handle reset button press"""
        self.servings_input.text = ''
        self.results_label.text = 'Enter servings and tap Scale Recipe'
        self.scaled_recipe = None
    
    def display_original_recipe(self):
        """Display original recipe (no scaling needed)"""
        result_text = "[b]No scaling needed![/b]\n\n"
        result_text += "[b]INGREDIENTS:[/b]\n"
        
        for ingredient, details in ORIGINAL_RECIPE.items():
            name = format_ingredient_name(ingredient)
            amount = format_amount(details["amount"])
            unit = details["unit"]
            result_text += f"  • {amount} {unit} {name}\n"
        
        self.results_label.text = result_text
    
    def display_scaled_recipe(self, recipe: dict, servings: int, scaling_factor: float):
        """Display scaled recipe results - mobile optimized"""
        result_text = f"[b]RECIPE FOR {servings} SERVINGS[/b]\n"
        result_text += f"[size=12sp](Scaling factor: {scaling_factor:.2f}x)[/size]\n\n"
        result_text += "[b]INGREDIENTS:[/b]\n"
        
        for ingredient, details in recipe.items():
            name = format_ingredient_name(ingredient)
            amount = format_amount(details["amount"])
            unit = details["unit"]
            result_text += f"  • {amount} {unit}  {name}\n"
        
        self.results_label.text = result_text
    
    def show_error(self, message: str):
        """Display error in popup - mobile friendly"""
        popup_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        error_label = Label(text=message, size_hint_y=0.8)
        popup_layout.add_widget(error_label)
        
        close_btn = Button(text='OK', size_hint_y=0.2)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(
            title='Input Error',
            content=popup_layout,
            size_hint=(0.9, 0.4)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


# ============================================================================
# APP ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    RecipeAdjusterApp().run()
