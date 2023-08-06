from .utils import D66
import json
import os


class NameGenerator:
    """
    Psychic Awakenings -based name generator
    """
    def __init__(self) -> None:
        
        # contains the data from name generators published in psychic awakenings during warhammer 40k v8
        with open(os.path.join(os.path.dirname(__file__), "namegen.json"), "r") as f:
            self.data = json.load(f)

        self.faction_to_langs = {
            faction: list(langs)
            for faction, langs in self.data.items()
        }

    def generate(self, faction, lang):
        if faction not in self.faction_to_langs.keys():
            raise ValueError(f"faction '{faction}' is not available")
        if lang not in self.faction_to_langs[faction]:
            raise ValueError(f"lang '{lang}' is not available for faction '{faction}'")
            
        table = self.data[faction][lang]
        front_bit = table[D66()]["front_bit"]
        uvver_bit = table[D66()]["uvver_bit"]

        return front_bit if not uvver_bit else f"{front_bit} {uvver_bit}"
