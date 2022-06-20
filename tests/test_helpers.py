from wtforms_bootstrap5.helpers import traverse_base_classes


def test_simple_traverse_base_classes():
    class A:
        pass

    assert traverse_base_classes(cls=A) == [(A,)]


def test_subclass_traverse_base_classes():
    class A:
        pass

    class B(A):
        pass

    assert traverse_base_classes(cls=B) == [
        (
            B,
            A,
        )
    ]


def test_mixedin_traverse_base_classes():
    class A:
        pass

    class B(A):
        pass

    class MixedIn:
        pass

    class C(MixedIn, B):
        pass

    assert traverse_base_classes(cls=C) == [
        (
            C,
            MixedIn,
        ),
        (
            C,
            B,
            A,
        ),
    ]
