from src.core.utils import get_object_str


class TestGetObjectStr:
    class Foo:
        attr_1 = 123

        def __init__(self):
            self.attr_2 = "SHOULD-NOT-BE-RETURNED"
            self.attr_3 = "string"

    def test_returns_correct_str(self):
        # GIVEN
        foo = self.Foo()

        # WHEN
        object_str = get_object_str(foo, attrs_to_show=["attr_1", "attr_3"])

        # THEN
        assert object_str == "Foo(attr_1=123, attr_3='string')"
