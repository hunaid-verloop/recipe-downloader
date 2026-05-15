import os
import argparse
import json
import csv
from concurrent.futures import ThreadPoolExecutor

import requests

LIST_RECIPES = "/gateway/twirp/verloop.gateway.recipe.RecipeService/ListRecipes"
GET_RECIPE = "/gateway/twirp/verloop.gateway.recipe.RecipeService/GetRecipe"

OUTPUT_DIR = os.path.join(os.getcwd(), "fetched_recipes")

auth_key = os.getenv('auth_key', '')



def listRecipes(base_url: str):
    url = base_url + LIST_RECIPES
    headers = {"content-type": "application/json",
               "authorization": auth_key,
               }
    payload = { "params": [] }
    resp = requests.post(
        url = url,
        json = payload,
        headers=headers
    ).json()
    return resp['Recipes']

def getRecipe(base_url: str, recipe_id: str):
    url = base_url + GET_RECIPE
    headers = {"content-type": "application/json",
               "authorization": auth_key,
               }
    payload = { "RecipeID": recipe_id }
    resp = requests.post(
        url = url,
        json = payload,
        headers=headers
    ).json()

    return resp

def fetch_and_save_recipe(base_url: str, recipe_id: str):
    recipe = getRecipe(base_url, recipe_id)
    file_name = os.path.join(OUTPUT_DIR, f'{recipe_id}.json')
    with open(file_name, 'w') as f:
        json.dump(recipe, f)


def build_id_name_map(base_url: str):
    recipe_list = listRecipes(base_url)
    recipe_id_list = [item['Meta']['Id'] for item in recipe_list]
    
    id_name = []
    for recipe_id in recipe_id_list:
        recipe = getRecipe(base_url, recipe_id)
        id_name.append({"recipe_id": recipe_id, "recipe_name": recipe['Recipe']['Name']})


    print(id_name)

    with open('id_name-mapping.csv', 'w', newline='') as csvfile:
        fieldnames = ['recipe_id', 'recipe_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(id_name)
    

def main(base_url: str, max_workers=3):
    recipe_list = listRecipes(base_url)
    recipe_id_list = [item['Meta']['Id'] for item in recipe_list]
    os.mkdir(OUTPUT_DIR)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_and_save_recipe, base_url, recipe_id) for recipe_id in recipe_id_list]
        for f in futures:
            f.result()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A basic greeting script.")
    parser.add_argument("--base_url", help="client dashboard")
    args = parser.parse_args()

    if auth_key == "":
        print("Please provide your authorization key to access the verloop api")
    else:
        print(args)
        print(args.base_url)
        # main(base_url=args.base_url)
        build_id_name_map(args.base_url)
