import os  # For interacting with the operating system (e.g., environment variables)
import sys  # For system-specific parameters and functions (e.g., exiting the script)
import google.generativeai as genai  # The Google Generative AI library
from google.genai.errors import APIError  # For handling API-related errors

# --- Configuration Section ---
# This section defines the API key and model name used for the Gemini API.
# The script automatically looks for the GEMINI_API_KEY environment variable.

API_KEY_NAME = 'GEMINI_API_KEY'  # The name of the environment variable storing the API key
MODEL_NAME = 'gemini-2.5-flash'  # The name of the Gemini model to use

# Check if the API key is set as an environment variable
if API_KEY_NAME not in os.environ:
    print(f"Error: The '{API_KEY_NAME}' environment variable is not set.")
    print("Please set your API key using: $env:GEMINI_API_KEY='YOUR_KEY' (Windows) or export GEMINI_API_KEY='YOUR_KEY' (Linux/macOS)")
    sys.exit(1)  # Exit the script if the API key is not set

# --- Gemini Client Initialisation ---
# This section initialises the Gemini client with the API key.
try:
    # Configure the API key using the value from the environment variable
    genai.configure(api_key=os.environ.get(API_KEY_NAME))

    # Access the specified Gemini model
    model = genai.GenerativeModel(MODEL_NAME)

except Exception as e:
    print(f"Error initialising Gemini client. Check your key and network connection: {e}")
    sys.exit(1)  # Exit the script if the client cannot be initialised

# --- User Input Section ---
# This section defines the function to gather user preferences for the recipe.
def get_user_preferences():
    """
    Gathers detailed user preferences for the recipe, including main ingredients,
    dietary needs, cuisine style, and maximum cooking time.
    """
    print("=" * 50)
    print("✨ Gemini Recipe Chef ✨")
    print("=" * 50)
    ingredients = input("🍽️ What main ingredients do you have? (e.g., chicken, broccoli, pasta): ").strip()  # Get main ingredients
    diet = input("🍎 Any dietary needs? (e.g., vegetarian, gluten-free, low-carb): ").strip()  # Get dietary needs
    cuisine = input("🌎 What cuisine or style? (e.g., Italian, Thai, comfort food): ").strip()  # Get cuisine style
    time = input("⏱️ Max cooking time? (e.g., 30 minutes, 1 hour): ").strip()  # Get maximum cooking time
    
    # Basic validation: Ensure that the main ingredients are provided
    if not ingredients:
        print("A main ingredient is required to generate a recipe.")
        sys.exit(1)  # Exit if no main ingredients are provided
        
    return ingredients, diet, cuisine, time  # Return the gathered preferences

# --- Prompt Construction Section ---
# This section defines the function to construct the prompt for the Gemini model.
def create_recipe_prompt(ingredients, diet, cuisine, time):
    """
    Constructs the full prompt for the Gemini model, including system instructions
    and user preferences. The prompt is designed to elicit a recipe with detailed
    cooking steps and nutritional information.
    """
    
    # System instruction defines the model's persona, constraints, and desired output format
    system_instruction = (
        "You are a professional chef and creative recipe developer. "
        "Your task is to generate a single, complete, and easy-to-follow recipe "
        "based on the user's specific inputs and constraints. "
        "The recipe MUST be structured as follows (EXAMPLE):\n\n"
        "**Recipe Title:** Delicious Chicken Stir-Fry\n\n"
        "**Ingredients:**\n"
        "- Chicken breast: 1 lb, cubed\n"
        "- Broccoli florets: 1 cup\n"
        "- Soy sauce: 2 tbsp\n"
        "- Ginger: 1 tsp, minced\n"
        "- Garlic: 2 cloves, minced\n"
        "- Cooked rice: 2 cups\n\n"
        "**Instructions:**\n"
        "Step 1: Heat a wok or large skillet over high heat.\n"
        "Step 2: Add the chicken and stir-fry until cooked through.\n"
        "Step 3: Add the broccoli, soy sauce, ginger, and garlic.\n"
        "Step 4: Stir-fry for another 3-5 minutes, until the broccoli is tender-crisp.\n"
        "Step 5: Serve over cooked rice.\n\n"
        "**Nutritional Information (per serving):**\n"
        "- Calories: Approximately 400\n"
        "- Protein: 30g\n"
        "- Fat: 15g\n"
        "- Carbohydrates: 40g\n\n"
        "Do not include any introductory or concluding remarks. Only provide the recipe in the specified format."
    )
    
    # Construct the main user prompt with preferences
    user_prompt = f"""
    Generate a recipe with the following characteristics:
    - **Main Ingredients:** {ingredients}
    - **Dietary Needs/Preferences:** {diet}
    - **Preferred Cuisine/Style:** {cuisine}
    - **Time Constraint:** {time}
    
    Ensure the recipe includes detailed cooking steps and nutritional information (calories, protein, fat, carbohydrates per serving) and adheres to the format specified in the system instructions.
    """
    
    return system_instruction, user_prompt  # Return the constructed prompt

# --- API Call and Output Section ---
# This section defines the function to generate the recipe using the Gemini API
# and print the output.
def generate_recipe():
    """
    Generates and prints the recipe using the Gemini API, handling potential errors
    and validating the response.
    """
    ingredients, diet, cuisine, time = get_user_preferences()  # Get user preferences

    system_instruction, user_prompt = create_recipe_prompt(
        ingredients, diet, cuisine, time
    )  # Construct the prompt

    print("\n--- Generating Recipe... This may take a moment. ---")
    
    try:
        # Use the generate_content method on the model object to generate the recipe
        response = model.generate_content(
            system_instruction + "\n" + user_prompt,  # Combine system and user prompts
            generation_config={
                "temperature": 0.8,  # Higher temperature for more creativity
                "max_output_tokens": 5012  # Increased token limit to allow for longer responses
            },
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"  
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"  
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"  
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"  
                },
            ]
        )

        print("\n" * 2 + "=" * 50)
        print("✅ RECIPE GENERATED SUCCESSFULLY")
        print("=" * 50)

        # Check if the response contains a valid text part before printing
        if response.parts and hasattr(response, 'text'):
            print(response.text.strip())  # Print the generated recipe
        else:
            print("⚠️ No valid recipe text found in the response.")
            print("Full Response:", response)  # Print the full response for debugging

        print("=" * 50)

    except APIError as e:
        print(f"\n[API Error] Could not generate recipe: {e}")
        print(f"Full API Response: {e}")  # Print the full error response
    except Exception as e:
        print(f"\n[Runtime Error] An unexpected error occurred: {e}")
        print(f"Full Exception: {e}")  # Print the full exception

# --- Main Execution ---
# This section ensures that the generate_recipe function is called when the script is run.
if __name__ == "__main__":
    generate_recipe()  # Call the generate_recipe function to start the process