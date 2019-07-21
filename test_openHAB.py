import responses
import json
import unittest
from openhab.openhab import OpenHAB, Item


def load_mocks() -> None:
    with open("test/items.json") as f:
        data = json.load(f)

    responses.add(
        responses.GET,
        'http://localhost:8080/rest/items?recursive=false&fields=name%2Clabel%2Ctype%2Ceditable%2Cmetadata&metadata=semantics%2Csynonyms',
        json=data,
        status=200
    )


class TestOpenHAB(unittest.TestCase):

    @responses.activate
    def test_init_openhab(self):
        load_mocks()
        oh = OpenHAB("http://localhost:8080")

    @responses.activate
    def test_get_location_by_tag(self):
        load_mocks()
        oh = OpenHAB("http://localhost:8080")
        location = oh.get_location("schlafzimmer")

        self.assertIsInstance(location, Item)
        self.assertTrue(location.is_location())
        self.assertFalse(location.is_equipment())
        self.assertFalse(location.is_point())

    @responses.activate
    def test_get_not_existing_location(self):
        load_mocks()
        oh = OpenHAB("http://localhost:8080")
        location = oh.get_location("NotExisting")

        self.assertIsNone(location)

    @responses.activate
    def test_get_injections(self):
        load_mocks()
        oh = OpenHAB("http://localhost:8080")
        injections = oh.get_injections()

        self.assertIsInstance(injections, tuple)
        self.assertEqual(len(injections), 2)

        items, locations = injections

        self.assertIsInstance(items, list)
        self.assertIsInstance(locations, list)

        self.assertIn("fernseher", items)
        self.assertNotIn("fernseher", locations)

        self.assertIn("schlafzimmer", locations)
        self.assertNotIn("schlafzimmer", items)


if __name__ == '__main__':
    unittest.main()
