package com.example.grandmawscookie

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.EditText
import android.widget.Button
import android.widget.TextView
import android.text.method.ScrollingMovementMethod

class MainActivity : AppCompatActivity() {
    
    private lateinit var servingsInput: EditText
    private lateinit var adjustButton: Button
    private lateinit var resultText: TextView
    
    // Original recipe for 4 servings
    private val originalRecipe = mapOf(
        "flour" to 2.0,
        "sugar" to 1.0,
        "butter" to 0.5,
        "eggs" to 1.0
    )
    private val originalServings = 4
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        servingsInput = findViewById(R.id.servings_input)
        adjustButton = findViewById(R.id.adjust_button)
        resultText = findViewById(R.id.result_text)
        resultText.movementMethod = ScrollingMovementMethod()
        
        adjustButton.setOnClickListener {
            adjustRecipe()
        }
    }
    
    private fun adjustRecipe() {
        val servingsStr = servingsInput.text.toString().trim()
        
        if (servingsStr.isEmpty()) {
            resultText.text = "Please enter a number of servings"
            return
        }
        
        try {
            val desiredServings = servingsStr.toDouble()
            
            if (desiredServings <= 0) {
                resultText.text = "Error: Servings must be greater than 0"
                return
            }
            
            // Calculate scaling factor
            val scaleFactor = desiredServings / originalServings
            
            // Scale the recipe
            val scaledRecipe = mutableMapOf<String, Double>()
            for ((ingredient, amount) in originalRecipe) {
                scaledRecipe[ingredient] = amount * scaleFactor
            }
            
            // Display results
            val result = StringBuilder()
            result.append("GRANDMA'S COOKIE RECIPE\n")
            result.append("Adjusted for: $desiredServings servings\n\n")
            result.append("ORIGINAL RECIPE (for 4 servings):\n")
            for ((ingredient, amount) in originalRecipe) {
                result.append("  • ${ingredient.replaceFirstChar { it.uppercase() }}: ${formatQuantity(amount, ingredient)}\n")
            }
            result.append("\nSCALED RECIPE (for $desiredServings servings):\n")
            for ((ingredient, amount) in scaledRecipe) {
                result.append("  • ${ingredient.replaceFirstChar { it.uppercase() }}: ${formatQuantity(amount, ingredient)}\n")
            }
            result.append("\nBAKING INSTRUCTIONS:\n")
            result.append("1. Mix all ingredients in a large bowl\n")
            result.append("2. Drop spoonfuls onto baking sheet\n")
            result.append("3. Bake at 350°F for 15 minutes\n")
            result.append("4. Cool on wire rack\n")
            result.append("5. Share with Grandma and enjoy!")
            
            resultText.text = result.toString()
            
        } catch (e: NumberFormatException) {
            resultText.text = "Error: Please enter a valid number"
        } catch (e: Exception) {
            resultText.text = "Error: ${e.message}"
        }
    }
    
    private fun formatQuantity(amount: Double, ingredientName: String): String {
        // Most ingredients are measured in cups, eggs are whole units
        val unit = if (ingredientName == "eggs") "egg" else "cup"
        
        // Pluralize the unit if needed
        val pluralUnit = if (amount != 1.0) "$unit" + "s" else unit
        
        // Format with 2 decimal places for clean display
        return String.format("%.2f %s", amount, pluralUnit)
    }
}
