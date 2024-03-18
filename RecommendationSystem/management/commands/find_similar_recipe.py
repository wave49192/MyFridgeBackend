import torch
import torch.nn.functional as F

#this is a mock recipe and ingredients
recipes = [
    "Berry Blast Smoothie",
    "Coconut Curry Chicken",
    "Classic Spaghetti Bolognese",
    "Mango Tango Salsa",
    "Cheesy Garlic Bread",
    "Greek Salad",
    "Stuffed Bell Peppers",
    "Teriyaki Salmon",
    "Caprese Salad",
    "Vegetable Stir Fry",
    "Blueberry Pancakes",
    "Chicken Alfredo Pasta",
    "Tropical Fruit Salad",
    "Spinach and Feta Stuffed Chicken Breasts",
    "Cajun Shrimp and Rice",
    "Chocolate Chip Cookies",
    "Grilled Cheese Sandwich",
    "Chicken Caesar Salad",
    "Beef Tacos",
    "Pumpkin Soup",
    "Apple Pie",
    "Lasagna",
    "Chicken Tikka Masala",
    "Guacamole",
    "French Toast",
    "Creamy Mushroom Risotto",
    "Beef Stroganoff",
    "Tomato Basil Bruschetta",
    "Crispy Baked Chicken Wings",
    "Ratatouille",
    "Honey Mustard Glazed Salmon",
    "Shrimp Scampi",
    "Vegetable Lasagna",
    "Spicy Thai Noodles",
    "Lemon Garlic Roast Chicken",
    "Beef and Broccoli Stir Fry",
    "Chocolate Lava Cake",
    "Eggplant Parmesan"
]
recipe_cuisines = {
    "Berry Blast Smoothie": "Smoothie",
    "Coconut Curry Chicken": "Indian",
    "Classic Spaghetti Bolognese": "Italian",
    "Mango Tango Salsa": "Mexican",
    "Cheesy Garlic Bread": "Italian",
    "Greek Salad": "Greek",
    "Stuffed Bell Peppers": "Mexican",
    "Teriyaki Salmon": "Japanese",
    "Caprese Salad": "Italian",
    "Vegetable Stir Fry": "Chinese",
    "Blueberry Pancakes": "American",
    "Chicken Alfredo Pasta": "Italian",
    "Tropical Fruit Salad": "American",
    "Spinach and Feta Stuffed Chicken Breasts": "Mediterranean",
    "Cajun Shrimp and Rice": "Cajun",
    "Chocolate Chip Cookies": "American",
    "Grilled Cheese Sandwich": "American",
    "Chicken Caesar Salad": "American",
    "Beef Tacos": "Mexican",
    "Pumpkin Soup": "American",
    "Apple Pie": "American",
    "Lasagna": "Italian",
    "Chicken Tikka Masala": "Indian",
    "Guacamole": "Mexican",
    "French Toast": "American",
    "Creamy Mushroom Risotto": "Italian",
    "Beef Stroganoff": "Russian",
    "Tomato Basil Bruschetta": "Italian",
    "Crispy Baked Chicken Wings": "American",
    "Ratatouille": "French",
    "Honey Mustard Glazed Salmon": "American",
    "Shrimp Scampi": "Italian",
    "Vegetable Lasagna": "Italian",
    "Spicy Thai Noodles": "Thai",
    "Lemon Garlic Roast Chicken": "Mediterranean",
    "Beef and Broccoli Stir Fry": "Chinese",
    "Chocolate Lava Cake": "American",
    "Eggplant Parmesan": "Italian"
    ,"Dog Food":"Dog",
}

ingredients = [
    ["mixed frozen berries", "natural yoghurt", "runny honey", "fresh mint"],
    ["coconut milk", "curry powder", "chicken breast", "garlic", "onion", "olive oil"],
    ["ground beef", "onion", "garlic", "canned tomatoes", "spaghetti pasta", "olive oil", "salt", "black pepper", "dried oregano"],
    ["mango", "red onion", "jalapeño pepper", "cilantro", "lime juice", "salt"],
    ["baguette", "butter", "garlic", "mozzarella cheese", "parsley"],
    ["cucumber", "tomato", "red onion", "kalamata olives", "feta cheese", "olive oil", "lemon juice", "dried oregano", "salt", "black pepper"],
    ["ground turkey", "bell peppers", "rice", "onion", "garlic", "tomato sauce", "mozzarella cheese", "salt", "black pepper"],
    ["salmon fillets", "soy sauce", "brown sugar", "garlic", "ginger", "sesame oil", "green onions"],
    ["tomatoes", "fresh mozzarella cheese", "fresh basil leaves", "balsamic vinegar", "olive oil", "salt", "black pepper"],
    ["broccoli", "bell peppers", "carrots", "snap peas", "onion", "garlic", "ginger", "soy sauce", "sesame oil", "rice vinegar"],
    ["flour", "baking powder", "salt", "milk", "eggs", "butter", "blueberries", "maple syrup"],
    ["chicken breast", "fettuccine pasta", "heavy cream", "Parmesan cheese", "garlic", "butter", "salt", "black pepper", "parsley"],
    ["pineapple", "mango", "kiwi", "strawberries", "honey", "lime juice", "mint leaves"],
    ["chicken breasts", "spinach", "feta cheese", "garlic", "olive oil", "salt", "black pepper"],
    ["shrimp", "bell peppers", "onion", "celery", "garlic", "rice", "chicken broth", "Cajun seasoning", "salt", "black pepper"],
    ["flour", "butter", "sugar", "egg", "vanilla extract", "chocolate chips", "baking soda", "salt"],
    ["bread", "butter", "cheese"],
    ["romaine lettuce", "chicken breast", "Caesar dressing", "Parmesan cheese", "croutons"],
    ["ground beef", "taco seasoning", "tortillas", "lettuce", "tomato", "cheese", "salsa"],
    ["pumpkin", "onion", "garlic", "vegetable broth", "coconut milk", "nutmeg", "cinnamon", "salt", "black pepper"],
    ["apples", "sugar", "cinnamon", "flour", "butter", "pie crust"],
    ["lasagna noodles", "ground beef", "ricotta cheese", "mozzarella cheese", "parmesan cheese", "tomato sauce", "onion", "garlic", "olive oil", "salt", "black pepper"],
    ["chicken breast", "tomato sauce", "coconut milk", "garam masala", "garlic", "ginger", "onion", "chili powder", "salt", "black pepper"],
    ["avocado", "tomato", "onion", "lime juice", "cilantro", "salt", "black pepper"],
    ["bread", "eggs", "milk", "vanilla extract", "cinnamon", "butter", "maple syrup"],
    ["arborio rice", "mushrooms", "chicken broth", "white wine", "onion", "garlic", "parmesan cheese", "butter", "salt", "black pepper"],
    ["beef sirloin", "onion", "mushrooms", "beef broth", "sour cream", "flour", "butter", "salt", "black pepper"],
    ["tomatoes", "garlic", "basil", "olive oil", "balsamic vinegar", "salt", "black pepper", "baguette"],
    ["chicken wings", "baking powder", "salt", "black pepper", "garlic powder", "paprika", "hot sauce", "butter"],
    ["eggplant", "tomatoes", "zucchini", "bell peppers", "onion", "garlic", "tomato sauce", "olive oil", "basil", "oregano", "salt", "black pepper"],
    ["salmon fillets", "honey", "dijon mustard", "lemon juice", "garlic", "salt", "black pepper"],
    ["shrimp", "linguine pasta", "garlic", "butter", "lemon juice", "white wine", "parsley", "red pepper flakes", "salt", "black pepper"],
    ["lasagna noodles", "zucchini", "yellow squash", "mushrooms", "ricotta cheese", "mozzarella cheese", "parmesan cheese", "tomato sauce", "onion", "garlic", "olive oil", "salt", "black pepper"],
    ["rice noodles", "bell peppers", "carrots", "snap peas", "garlic", "ginger", "soy sauce", "sriracha", "brown sugar", "lime juice", "cilantro", "salt", "black pepper"],
    ["chicken", "lemon", "garlic", "thyme", "rosemary", "butter", "salt", "black pepper"],
    ["beef sirloin", "broccoli", "bell peppers", "onion", "garlic", "ginger", "soy sauce", "brown sugar", "sesame oil", "cornstarch", "rice vinegar", "salt", "black pepper"],
    ["chocolate", "butter", "sugar", "eggs", "vanilla extract", "flour", "salt"],
    ["eggplant", "flour", "eggs", "breadcrumbs", "marinara sauce", "mozzarella cheese", "parmesan cheese", "salt", "black pepper"]
    , ["eggplant", "flour", "eggs", "breadcrumbs", "marinara sauce", "mozzarella cheese", "parmesan cheese", "salt", "black pepper"]
]

# Create a vocabulary of unique ingredients
ingredient_vocab = {ingredient: i for i, ingredient in enumerate(set([ingredient for recipe in ingredients for ingredient in recipe]))}

# Function to convert ingredients and cuisine to one-hot vectors
def recipe_to_onehot(recipe_name):
    onehot_ingredient = torch.zeros(len(ingredient_vocab))
    for ingredient in ingredients[recipes.index(recipe_name)]:
        index = ingredient_vocab[ingredient]
        onehot_ingredient[index] = 1
    
    onehot_cuisine = torch.zeros(len(set(recipe_cuisines.values())))
    index = list(set(recipe_cuisines.values())).index(recipe_cuisines[recipe_name])
    onehot_cuisine[index] = 1
    
    return torch.cat((onehot_ingredient, onehot_cuisine))

# Convert all recipes' ingredients and cuisine to one-hot vectors
recipe_vectors = torch.stack([recipe_to_onehot(recipe) for recipe in recipes])
# Function to find similar recipes based on ingredient similarity
def find_similar_recipes_by_ingredients(favorite_recipe_indices, top_n=5):
    avg_recipe_vector = torch.mean(torch.stack([recipe_vectors[i] for i in favorite_recipe_indices]), dim=0)
    similarity_scores = F.cosine_similarity(recipe_vectors[:, :-len(set(recipe_cuisines.values()))], avg_recipe_vector[:-len(set(recipe_cuisines.values()))].unsqueeze(0))
    
    # Exclude favorite recipes from recommendations
    for index in favorite_recipe_indices:
        similarity_scores[index] = -1  # Set similarity score to -1 for favorite recipes
    
    top_indices = similarity_scores.argsort(descending=True)[:top_n]
    return [(recipes[i], similarity_scores[i].item()) for i in top_indices]

# Function to find similar recipes based on cuisine type similarity
def find_similar_recipes_by_cuisine(favorite_recipe_indices, top_n=5):
    avg_recipe_vector = torch.mean(torch.stack([recipe_vectors[i] for i in favorite_recipe_indices]), dim=0)
    similarity_scores = F.cosine_similarity(recipe_vectors[:, -len(set(recipe_cuisines.values())):], avg_recipe_vector[-len(set(recipe_cuisines.values())):].unsqueeze(0))
    
    # Exclude favorite recipes from recommendations
    for index in favorite_recipe_indices:
        similarity_scores[index] = -1  # Set similarity score to -1 for favorite recipes
    
    top_indices = similarity_scores.argsort(descending=True)[:top_n]
    return [(recipes[i], similarity_scores[i].item()) for i in top_indices]

# Example usage:
favorite_recipe_indices = [recipes.index("Eggplant Parmesan"),recipes.index("Grilled Cheese Sandwich")]


print("Recommendations Based on Ingredient Similarity:")
similar_recipes_by_ingredients = find_similar_recipes_by_ingredients(favorite_recipe_indices)
for recipe, similarity in similar_recipes_by_ingredients:
    print(f"{recipe}: Similarity Score = {similarity:.4f}")

print("\nRecommendations Based on Cuisine Type Similarity:")
similar_recipes_by_cuisine = find_similar_recipes_by_cuisine(favorite_recipe_indices)
for recipe, similarity in similar_recipes_by_cuisine:
    print(f"{recipe}: Similarity Score = {similarity:.4f}")
