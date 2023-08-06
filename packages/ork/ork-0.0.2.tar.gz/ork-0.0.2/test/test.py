import unittest

from parameterized import parameterized

from ork import NameGenerator


class Test(unittest.TestCase):
    ng = NameGenerator()

    @parameterized.expand([
        [faction, lang]
        for faction, langs in ng.faction_to_langs.items()
        for lang in langs
    ])
    def test_generate(self, faction, lang):
        print(self.ng.generate(faction=faction, lang=lang))

    def test_generate_error(self):
        self.assertRaises(ValueError, lambda: NameGenerator().generate(faction="orks", lang="it"))
