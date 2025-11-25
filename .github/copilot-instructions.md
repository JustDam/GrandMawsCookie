# Grand Maws Cookie Recipe Adjuster - AI Agent Guidelines

## Project Overview

**Grand Maws Cookie** is a dual-implementation recipe scaling application that adjusts ingredient quantities based on desired servings. The original recipe serves 12 people and uses a linear scaling model for all ingredients.

**Architecture:** Logic-UI separation with shared core functions deployed across three implementations:
- `GrandMawsCookie.py` – Console version (primary reference)
- `GrandMawsCookie_Console_Working.py` – Console version (backup)
- `GrandMawsCookie_APK.py` – Mobile/Kivy version for Android deployment

## Core Principles & Patterns

### 1. **Design-by-Contract with Assertions**
Every function uses explicit preconditions, postconditions, and sanity checks via `assert` statements. This is NOT optional:
- Always validate input types and ranges before processing
- Assert expected postconditions after transformations
- Use descriptive assertion messages with actual vs. expected values
- Example: `assert isinstance(amount, (int, float)), f"Amount must be numeric, got {type(amount)}"`

### 2. **Data Structure: Recipe Dictionary**
All recipes use a consistent nested dictionary format—**do not deviate**:
```python
recipe = {
    "ingredient_name": {"amount": float_value, "unit": "string"},
    "flour": {"amount": 3.0, "unit": "cups"},
    "sugar": {"amount": 2.0, "unit": "cups"}
}
```
Keys must be snake_case. Never add or remove dict keys during transformation. Validate structure in `scale_recipe()` before processing.

### 3. **Fraction Formatting**
The `format_amount()` function uses a lookup table for common fractions:
```python
fractions = {0.25: "1/4", 0.33: "1/3", 0.5: "1/2", 0.66: "2/3", 0.75: "3/4"}
```
- Whole numbers (2.0) → "2"
- Mixed numbers (1.5) → "1 1/2"
- Uncommon decimals → rounded to 2 places ("2.33")
- When modifying: **always round decimals to 2 places** before dict lookup to catch edge cases

### 4. **Input Validation Pattern**
Use `is_valid_servings()` as the model for all user input validation:
- Returns tuple: `(is_valid: bool, error_message: str, parsed_value: int)`
- Validates type, range (MIN_SERVINGS=1, MAX_SERVINGS=100), and whole-number constraint
- Rejects decimals, negative values, empty strings
- Always call before downstream calculations

### 5. **Scaling is Linear and Multiplicative**
The scaling factor is simply `desired_servings / original_servings`:
```python
scaling_factor = calculate_scaling_factor(ORIGINAL_SERVINGS, desired_servings)
# Then: scaled_recipe[ingredient]["amount"] = original_recipe[ingredient]["amount"] * scaling_factor
```
**Critical:** Scaling preserves units; units are never transformed (cups stay cups, tsp stays tsp).

## File-Specific Guidance

### `GrandMawsCookie.py` (Console) – Primary Reference
- Entry point: `recipe_adjuster()` function (main loop)
- Includes full `run_tests()` suite for validation
- Has comparison display logic (`compare_recipes()`) for before/after side-by-side
- Use as the canonical implementation for logic; console-specific I/O can be ported to other UIs

### `GrandMawsCookie_APK.py` (Kivy Mobile)
- **Critical:** All calculation functions are **unchanged duplicates** from console version
- Kivy UI is in `RecipeAdjusterApp` class inheriting from `kivy.app.App`
- Key mobile adaptations:
  - `Window.size = (400, 800)` sets mobile-first dimensions
  - `TextInput` with `input_filter='int'` restricts keyboard to numbers
  - `ScrollView` wraps results label for small screens (scrollable output)
  - `Popup` widgets display errors instead of printing
  - Portrait orientation only (set in `buildozer.spec`)
- **When modifying:** Update calculation functions in BOTH console AND APK files to maintain sync

### Build & Deployment

**Android APK Build Process** (see `APK_BUILD_GUIDE.md`):
1. Requires: Python 3.9+, Java JDK 11+, Android SDK
2. Install: `pip install kivy==2.2.1 buildozer==1.5.0 cython`
3. Build: `buildozer android debug` (Linux/Mac recommended due to toolchain compatibility)
4. Install: `adb install -r bin/grandmawscookie-1.0.0-debug.apk`

**Critical `buildozer.spec` settings:**
- `main.py = GrandMawsCookie_APK.py` (entry point must point to Kivy version)
- `android.minapi = 21` (Android 5.0+)
- `orientation = portrait` (fixed for recipe display)
- `requirements = python3,kivy,android`

## Common Modification Patterns

### Adding an Ingredient
1. Add to `ORIGINAL_RECIPE` dict in **both** console and APK files
2. Maintain `{"amount": float, "unit": "string"}` structure
3. Use snake_case key names (e.g., `"baking_powder"`, not `"bakingPowder"`)
4. Reassert in startup validation that `ORIGINAL_RECIPE` is non-empty and well-formed
5. Add unit test in `run_tests()` to verify scaling works with new ingredient

### Changing Serving Limits
- Modify `MIN_SERVINGS`, `MAX_SERVINGS`, `ORIGINAL_SERVINGS` constants in **both** files
- Update bounds check in `is_valid_servings()`
- Update error messages and UI hints (e.g., `TextInput hint_text`)
- Add assertions to validate `ORIGINAL_SERVINGS` is within new bounds

### UI Changes (APK Only)
- New widgets go in `RecipeAdjusterApp.build()` method
- Bind button callbacks with `.bind(on_press=method_name)`
- Use `Popup` for modals (errors, confirmations)
- Test on emulator or device; layout is responsive via `size_hint_y` proportions

### Testing New Logic
- Add test cases to `run_tests()` function
- Test functions must include both happy path and edge cases (zero, negative, boundary values)
- Run with: `python GrandMawsCookie_Console_Working.py` (uncomment `run_tests()` in `__main__`)
- Assertions will catch errors; let them fail loudly

## Dependencies & Environment

- **Python:** 3.9+
- **Core:** No external dependencies for console version
- **Mobile:** Kivy 2.2.1, Buildozer 1.5.0
- **Build Requirements:** Java JDK 11+, Android SDK (for APK)
- **No network calls, no database, no async operations**

## Key Constants & Ranges

```python
ORIGINAL_SERVINGS = 12      # Baseline recipe size
MIN_SERVINGS = 1            # Cannot scale to 0 or negative
MAX_SERVINGS = 100          # Practical upper limit (prevents nonsense scaling)
ORIGINAL_RECIPE = {...}     # 8 ingredients (flour, sugar, butter, eggs, milk, baking_powder, vanilla_extract, salt)
```

All calculations use these constants; they are the single source of truth. Update them, not hardcoded values elsewhere.

## Error Handling Philosophy

- **Input validation errors** → return user-friendly message from validation functions, don't crash
- **Assertion failures** → intentional crashes with descriptive message (developers need to see broken contracts)
- **Scaling anomalies** → catch with sanity checks (e.g., scaled amount > 10000 is unreasonable)
- **Kivy-specific** → use `Popup` for user errors, not console print

## Testing Checklist

Before committing changes:
- [ ] Run `run_tests()` in console version (all tests pass)
- [ ] Test console version with edge case inputs (0, 1, 100, 150, decimals, letters)
- [ ] If modifying APK: build locally with `buildozer android debug` and test on emulator
- [ ] Verify calculation functions are identical in both console and APK files
- [ ] Check assertions are firing on invalid data
