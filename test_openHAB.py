import responses
import json
import unittest
from openhab.openhab import OpenHAB


class TestOpenHAB(unittest.TestCase):
    def load_mocks(self) -> None:
        with open("test/mock.json") as f:
            data = json.load(f)

        responses.add(
            responses.GET,
            'http://localhost:8080/rest/items?recursive=false&fields=name%2Clabel%2Ctype%2Ceditable%2Cmetadata&metadata=semantics%2Csynonyms',
            json=data,
            status=200
        )

    @responses.activate
    def test_init_openhab(self):
        self.load_mocks()
        oh = OpenHAB("http://localhost:8080")


if __name__ == '__main__':
    unittest.main()
