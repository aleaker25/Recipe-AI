# 👨‍🍳 Gemini Recipe Chef

A beginner-friendly **Python** project that uses the **Google Gemini API** to generate highly personalized recipes based on your ingredients, dietary constraints, preferred cuisine, and cooking time limits.

---

## ✨ Features

*   **Personalized Recipes:** Generates a unique recipe tailored to your specific input constraints.
*   **Structured Output:** Uses Gemini's System Instructions to enforce a clean format: Title, Ingredients (with quantities), Step-by-Step Instructions, and Estimated Nutritional Information.
*   **Ingredient Focus:** Ensures the generated recipe utilizes the ingredients you currently have on hand.
*   **Secure Authentication:** Reads the API key securely from an environment variable (`GEMINI_API_KEY`).

---

## 🛠️ Technology Stack

| Component           | Detail                                  |
| :------------------ | :-------------------------------------- |
| **Language**          | Python 3.9+                             |
| **AI Model**          | Google Gemini (`gemini-2.5-flash`)      |
| **Library**           | Google GenAI SDK (`google-generativeai`) |

---

## 🚀 Getting Started

Follow these steps to set up and run the Gemini Recipe Chef on your local machine.

### 1. Installation

**Create the project folder:**

  `mkdir gemini-recipe-chef`  
  `cd gemini-recipe-chef`


## Create and activate a virtual environment:  

`python -m venv venv`  

## Activate the virtual environment:  

On Windows (PowerShell/Command Prompt):  

`.\venv\Scripts\activate` 

On Linux/macOS:  

`source venv/bin/activate`  

Install Dependencies:  

`pip install google-generativeai`  

The script requires your Gemini API key to be set as an environment variable named GEMINI_API_KEY.

| Operating System            | Command to Set Key                                  |
| :------------------ | :-------------------------------------- |
| Windows (PowerShell)    |    $env:GEMINI_API_KEY="YOUR_API_KEY_HERE"                   |
| Linux/macOS (Bash/Zsh)          | export GEMINI_API_KEY="YOUR_API_KEY_HERE"      |

⚠️ Security Warning: Replace "YOUR_API_KEY_HERE" with the key you generated.
