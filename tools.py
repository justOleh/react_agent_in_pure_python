import json
import random

from langchain_core.utils.function_calling import convert_to_openai_tool


class Tool:
    def __init__(self, function):
        self.__function = function
        self.json_schema = self.__create_json_schema(self.__function)

    def __create_json_schema(self, function):
        return convert_to_openai_tool(function)

    def __repr__(self):
        return json.dumps(self.json_schema, indent=2)

    def __call__(self, *args, **kwargs):
        return self.__function(*args, **kwargs)

    def get_function_name(self):
        return self.json_schema["function"]["name"]

    def to_dict(self):
        return self.json_schema


def get_random_genre():
    genres = [ "Solarpunk Noir", "Mythic Cyber-Western", "Post-Apocalyptic Cozy Mystery", "Oceanic Space Opera", "Gothic Biopunk Romance", "Time-Loop Courtroom Drama", "Archaeological Horror Fantasy", "Retro-Futurist Pirate Adventure", "Desert Steampunk Epic", "Quantum Heist Thriller", "Folklore Detective Procedural", "Climate Fiction Survival Saga", "Dreamwave Coming-of-Age", "Neo-Victorian Monster Comedy", "Urban Shaman Action", "Lunar Colony Political Satire", "Whimsical Dark Academia", "AI Monastic Mystery", "Interdimensional Road-Trip Drama", "Eco-Mythological Adventure" ]
    return random.choice(genres)

random_genre_tool = Tool(get_random_genre)

tools = [random_genre_tool]