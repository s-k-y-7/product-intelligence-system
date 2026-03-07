from .dummyjson import DummyJsonCollector
from .fakestore import FakeStoreCollector


class CollectorFactory:

    COLLECTOR_MAP = {
        "dummyjson": DummyJsonCollector,
        "fakestore": FakeStoreCollector,
    }

    @classmethod
    def get_collector(cls, code):
        if code not in cls.COLLECTOR_MAP:
            raise ValueError(f"No collector for source code: {code}")

        return cls.COLLECTOR_MAP[code]()