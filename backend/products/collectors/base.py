#abstraction
class BaseCollector:
    def collect(self, product_source):
        raise NotImplementedError(
            "Collectors must implement collect() method"
        )