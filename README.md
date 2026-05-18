# Recipe Block Transformer

This repository provides utilities to transform and simplify recipe blocks from recipes built on the Verloop platform, making them easier for humans to read, analyze, and inspect.

## Repository Structure

- `example_blocks/`  
  Contains the original JSON representations of recipe blocks.

- `transformed_blocks/`  
  Contains the transformed and simplified versions of the recipe block JSON files.

- `recipe_processor.py`  
  Processes a recipe by simplifying each recipe block and returning the result as a Python dictionary containing the transformed blocks.

- `recipes_downloader.py`  
  Downloads all recipes from a given dashboard URL, simplifies them, and saves the transformed JSON files into the `fetched_recipes/` directory. The directory is created automatically if it does not already exist.


## Purpose

The transformation process reduces the complexity of raw recipe block JSON, making it more suitable for:

- Manual inspection
- Debugging
- Analysis and auditing
- Documentation and sharing

