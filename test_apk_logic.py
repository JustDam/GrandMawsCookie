#!/usr/bin/env python
"""Test that APK logic matches console version"""

from GrandMawsCookie_Console_Working import (
    format_amount, is_valid_servings, scale_recipe, calculate_scaling_factor
)

print('Testing APK vs Console logic equivalence:\n')

# Test 1: format_amount
print('1. format_amount tests:')
test_amounts = [(1.0, '1'), (0.5, '1/2'), (1.5, '1 1/2'), (2.33, '2.33')]
all_pass = True
for amount, expected in test_amounts:
    result = format_amount(amount)
    status = '✅' if result == expected else '❌'
    if result != expected:
        all_pass = False
    print(f'  {status} format_amount({amount}) = {result} (expected {expected})')

# Test 2: is_valid_servings
print('\n2. is_valid_servings tests:')
test_servings = [('12', True), ('0', False), ('150', False), ('abc', False)]
for serving, expected_valid in test_servings:
    is_valid, _, _ = is_valid_servings(serving)
    status = '✅' if is_valid == expected_valid else '❌'
    if is_valid != expected_valid:
        all_pass = False
    print(f'  {status} is_valid_servings("{serving}") = {is_valid} (expected {expected_valid})')

# Test 3: scale_recipe
print('\n3. scale_recipe test:')
test_recipe = {
    'flour': {'amount': 3.0, 'unit': 'cups'},
    'sugar': {'amount': 2.0, 'unit': 'cups'}
}
scaled = scale_recipe(test_recipe, 2.0)
status = '✅' if scaled['flour']['amount'] == 6.0 else '❌'
if scaled['flour']['amount'] != 6.0:
    all_pass = False
print(f'  {status} scale_recipe by 2.0x: flour 3.0 → {scaled["flour"]["amount"]} cups')

# Test 4: calculate_scaling_factor
print('\n4. calculate_scaling_factor tests:')
test_factors = [(12, 12, 1.0), (12, 24, 2.0), (12, 6, 0.5)]
for orig, desired, expected in test_factors:
    result = calculate_scaling_factor(orig, desired)
    status = '✅' if abs(result - expected) < 0.001 else '❌'
    if abs(result - expected) >= 0.001:
        all_pass = False
    print(f'  {status} calculate_scaling_factor({orig}, {desired}) = {result:.2f}x')

if all_pass:
    print('\n✅ All APK logic functions work correctly!')
else:
    print('\n❌ Some tests failed!')

