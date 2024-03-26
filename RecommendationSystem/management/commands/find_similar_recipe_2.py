from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationSystem:
    
    """
    The similarity score are high in the recipe that has a lot of ingredient and low in little ingredient, will fix later.
    The time complexity is high and can not be improved as it needs to do a nested loop in order to compare every word in the list 
    So I will find another way to improve the time complexity by using another algorithm.
    
    -----------UPDATE-------------
    TF-IDF Vectorization then cosine similarity. works fine on single favourite recipe.
    -----------UPDATE-------------
    
    Algorithm tried:
    1 Nltk distance (The Levenshtein distance between two strings: more distance = less alike).
    2 TF-IDF Vectorization then cosine similarity.
    """
    @staticmethod
    def recommend_similar_recipes(favorite_recipes):
        recipes_queryset = Recipe.objects.all()
        recipes = [
            {
                'recipe_id': recipe.recipe_id,
                'title': recipe.title,
                'cuisine_type': recipe.cuisine_type,
                'cleaned_ingredients': recipe.cleaned_ingredients
            }
            for recipe in recipes_queryset
        ]
        
        # Extracting favorite ingredients and ingredients for each recipe
        favorite_ingredients = [ingredient.strip() for favorite_recipe in favorite_recipes for ingredient in favorite_recipe['cleaned_ingredients'].split(',')]
        recipe_ingredients = [recipe['cleaned_ingredients'] for recipe in recipes]
        
        # Create TF-IDF vectors
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(recipe_ingredients + [' '.join(favorite_ingredients)])
        
        # Calculate cosine similarity between user's favorite ingredients and recipes
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        
        # Associate similarity scores with recipes
        recipe_similarity_scores = {recipes[i]['recipe_id']: similarity_scores[0][i] for i in range(len(recipes))}
        
        # Exclude favorite recipes from recommendations by setting their scores to 0
        for favorite_recipe in favorite_recipes:
            recipe_id = favorite_recipe['recipe_id']
            if recipe_id in recipe_similarity_scores:
                recipe_similarity_scores[recipe_id] = 0

        
        # Sort recipes based on similarity score
        sorted_recipes = sorted(recipes, key=lambda x: recipe_similarity_scores[x['recipe_id']], reverse=True)

        # Print recommended recipes
        print("Top 10 similar recipes:")
        for i, recipe in enumerate(sorted_recipes[:50], 1):
            print(f"{i}. {recipe['title']} (similarity score: {recipe_similarity_scores[recipe['recipe_id']]:.4f})")

class Command(BaseCommand):
    help = 'Recommend similar recipes based on a favorite recipe'

    def handle(self, *args, **kwargs):
        favorite_recipe = [
    {
        "recipe_id": "5ed6604591c37cdc054bca02",
        "title": "Crusty cheddar pies",
        "cuisine_type": "Cuban",
        "cleaned_ingredients": "slim young leeks thickly sliced, broccoli cut into small florets, celery sticks de-stringed and sliced, floury potatoes such as king edward cut into even-sized chunks, butter, pot 0% fat greek yogurt, ml semi-skimmed milk, plain flour, english mustard, wholegrain mustard, pack mature cheddar finely grated, None  Handful frozen peas"
    }
            ,      {
        "recipe_id": "5ed6604591c37cdc054bcaa7",
        "title": "Cucumber and Feta Rolls",
        "cuisine_type": "Korean",
        "cleaned_ingredients": "crumbled feta crumbled, greek yogurt, sundried tomatoes chopped, kalamata olives chopped, roasted red peppers chopped, oregano or dill chopped, lemon juice, None  Pepper to taste, cucumbers sliced thinly lengthwise"
    },
             {
        "recipe_id": "5ed6604591c37cdc054bc878",
        "title": "Deep-Dish Winter Fruit Pie with Walnut Crumb",
        "cuisine_type": "Korean",
        "cleaned_ingredients": "all-purpose flour, granulated sugar, fine sea salt, cold unsalted butter cut into 1/2-inch cubes, ice water, freshly squeezed lemon juice, all-purpose flour, packed brown sugar, raw walnuts coarsely chopped, ground cinnamon, fine sea salt, unsalted butter melted, dried figs, small apples peeled cored and sliced 1/inch thick, pears peeled cored and sliced 1/inch thick, cranberries fresh or frozen, granulated sugar, cornstarch"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc898",
        "title": "Delicious Ham and Potato Soup",
        "cuisine_type": "Mexican",
        "cleaned_ingredients": "peeled and diced potatoes, diced celery, finely chopped onion, diced cooked ham, water, chicken bouillon granules, salt or to taste, ground white or black pepper or to taste, butter, all-purpose flour, milk"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcc60",
        "title": "Delicious Hot Chocolate",
        "cuisine_type": "Filipino",
        "cleaned_ingredients": "milk, half-and-half, good semi sweet chocolate chips, sugar, None  Variations: orange rind orange syrup cinnamon sticks raspberry syrup abuelita chocolate mint extract peppermint patties whipped cream chocolate shavings"
    },
    {
        "recipe_id": "5ed6604691c37cdc054bd01b",
        "title": "Devilled tofu kebabs",
        "cuisine_type": "Russian",
        "cleaned_ingredients": "shallots or button onions, small new potatoes, tomato pure, light soy sauce, sunflower oil, clear honey, wholegrain mustard, firm smoked tofu cubed, courgette peeled and sliced, red pepper deseeded and diced"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcf56",
        "title": "Donut Chips",
        "cuisine_type": "Brazilian",
        "cleaned_ingredients": "soft glazed donut holes, cinnamon sugar"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc899",
        "title": "Donut Muffins",
        "cuisine_type": "Turkish",
        "cleaned_ingredients": "white sugar, margarine melted, ground nutmeg, milk, baking powder, all-purpose flour, margarine melted, white sugar, ground cinnamon"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc97e",
        "title": "Donut Muffins Recipe",
        "cuisine_type": "Vietnamese",
        "cleaned_ingredients": "granulated sugar, ground cinnamon, unsalted butter melted, all-purpose flour plus more for coating the pan, baking powder, fine salt, freshly ground nutmeg, baking soda, whole milk at room temperature, buttermilk at room temperature, unsalted butter at room temperature, plus granulated sugar, large eggs at room temperature"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcd2c",
        "title": "Double Broccoli Quinoa",
        "cuisine_type": "Argentinian",
        "cleaned_ingredients": "cooked quinoa*, raw broccoli cut into small florets and stems, medium garlic cloves, sliced or slivered almonds toasted, freshly grated parmesan, big pinches salt, fresh lemon juice, olive oil, heavy cream, None  Optional toppings: slivered basil fire oil ** sliced avocado, None  Crumbled feta or goat cheese"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc89a",
        "title": "Double Crust Stuffed Pizza",
        "cuisine_type": "Moroccan",
        "cleaned_ingredients": "white sugar, warm water, active dry yeast, olive oil, salt, all-purpose flour, can crushed tomatoes, packed brown sugar, garlic powder, olive oil, salt, shredded mozzarella cheese divided, pound bulk italian sausage, package sliced pepperoni, package sliced fresh mushrooms, green bell pepper chopped, red bell pepper chopped"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc89b",
        "title": "Double Tomato Bruschetta",
        "cuisine_type": "Japanese",
        "cleaned_ingredients": "roma tomatoes chopped, sun-dried tomatoes packed in oil, cloves minced garlic, olive oil, balsamic vinegar, fresh basil stems removed, salt, ground black pepper, french baguette, shredded mozzarella cheese"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcd93",
        "title": "Doughnuts with Grapefruit-Vanilla Jelly",
        "cuisine_type": "Japanese",
        "cleaned_ingredients": "sugar, fresh grapefruit juice, liquid pectin, vanilla bean split lengthwise, olive oil plus more for bowl, apple juice, 1/4-oz envelope active dry yeast, all-purpose flour plus more, plus sugar, large eggs, finely grated grapefruit zest, kosher salt, None  Vegetable oil"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc8fd",
        "title": "Hummus Pizza",
        "cuisine_type": "Greek",
        "cleaned_ingredients": "can refrigerated pizza crust dough, hummus spread, sliced bell peppers any color, broccoli florets, shredded monterey jack cheese"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc92f",
        "title": "Dr. Pepper Barbecue Sauce",
        "cuisine_type": "Mexican",
        "cleaned_ingredients": "unsalted butter, large yellow onion chopped, cloves garlic chopped, ketchup, tomato paste, None  One 12-oz can dr. pepper, cider vinegar, worcestershire sauce, packed dark brown sugar, ancho or new mexican chili powder, fine-ground white pepper, kosher salt"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bceaf",
        "title": "Drunken Watermelon Pops Recipe",
        "cuisine_type": "Russian",
        "cleaned_ingredients": "vodka, chambord or other raspberry-flavored liqueur, vanilla bean split lengthwise and scraped seeds reserved, seedless watermelon peeled and cut into large dice"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bc97c",
        "title": "Duck  l'Orange",
        "cuisine_type": "American",
        "cleaned_ingredients": "pekin duck, yellow onion coarsely chopped, sprigs thyme, celery stalk coarsely chopped, medium carrot peeled halved lengthwise then crosswise, whole black peppercorns, navel oranges, None  Kosher salt freshly ground pepper, port"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcf35",
        "title": "Duck Confit Fried Spring Rolls Recipe",
        "cuisine_type": "Argentinian",
        "cleaned_ingredients": "hoisin sauce, plum sauce, rice vinegar, soy sauce, None  Freshly ground black pepper, duck confit legs, quarts vegetable oil, cremini mushrooms stems trimmed and thinly sliced, None  Kosher salt, None  Freshly ground black pepper, medium carrot peeled and cut into matchsticks, medium yellow onion thinly sliced, five-spice powder, sliced water chestnuts thinly sliced into matchsticks, finely chopped fresh cilantro, round rice paper wrappers"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcf41",
        "title": "Duck Confit Salad with Cranberry Vinaigrette",
        "cuisine_type": "German",
        "cleaned_ingredients": "mixed salad greens, shredded duck confit, ripe avocado, pomegranate, tb. cranberry preserves, tb. apple cider vinegar, olive oil, None  Salt and pepper"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcaa8",
        "title": "Duck Quesadillas with Chipotle Cherry Salsa and Goat Cheese",
        "cuisine_type": "German",
        "cleaned_ingredients": "butter, chipotle pan seared duck breast sliced into small pieces, chipotle cherry salsa, green onion sliced, cilantro chopped, handful jack cheese grated, goat cheese room temperature, tortillas"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcaa9",
        "title": "Duck Tacos with Chipotle Cherry Salsa and Goat Cheese",
        "cuisine_type": "Mediterranean",
        "cleaned_ingredients": "pound duck breast, chipotle chili powder, cumin toasted and ground, salt to taste, chipotle cherry salsa, small corn tortillas lightly toasted, red cabbage thinly sliced and tossed in sour cream, goat cheese crumbed, None  Cress sprouts for garnish, cherries pitted, chipotle chili in adobo or to taste chopped, red onion diced, small clove garlic grated, handful basil, balsamic vinegar, None  Salt and pepper to taste"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcd64",
        "title": "Duck a l",
        "cuisine_type": "American",
        "cleaned_ingredients": "pekin duck, yellow onion coarsely chopped, sprigs thyme, celery stalk coarsely chopped, medium carrot peeled halved lengthwise then crosswise, whole black peppercorns, navel oranges, None  Kosher salt freshly ground pepper, port"
    },
    {
        "recipe_id": "5ed6604591c37cdc054bcfb6",
        "title": "Duck stir-fry with ginger & greens",
        "cuisine_type": "Peruvian",
        "cleaned_ingredients": "None  Groundnut oil, skinless duck breasts cut into thin strips, finely chopped ginger, red chilli sliced, spring onions sliced, pak choi sliced, soy sauce, honey, oyster sauce, cornflour"
    },
        ]

        self.stdout.write("Finding similar recipes...\n")
        RecommendationSystem.recommend_similar_recipes(favorite_recipe)
