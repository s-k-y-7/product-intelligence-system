from .dummyjson import DummyJsonCollector
from .fakestore import FakeStoreCollector
from .local_ecommerce_collector import LocalEcommerceCollector
from .local_ecommerce_2_collector import LocalEcommerceCollector_2



class CollectorFactory:

    COLLECTOR_MAP = {
        "dummyjson": DummyJsonCollector,
        "fakestore": FakeStoreCollector,
        "local_ecommerce": LocalEcommerceCollector,
        "local_ecommerce_2": LocalEcommerceCollector_2
    }

    @classmethod
    def get_collector(cls, code):
        if code not in cls.COLLECTOR_MAP:
            raise ValueError(f"No collector for source code: {code}")

        return cls.COLLECTOR_MAP[code]()