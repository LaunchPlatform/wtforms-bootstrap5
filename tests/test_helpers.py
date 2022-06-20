from wtforms_bootstrap5.helpers import traverse_base_classes


def test_simple_traverse_base_classes():
    class A:
        pass

    all_paths = []
    traverse_base_classes(cls=A, all_paths=all_paths)
    assert all_paths == [(A, object)]


def test_subclass_traverse_base_classes():
    class A:
        pass

    class B(A):
        pass

    all_paths = []
    traverse_base_classes(cls=B, all_paths=all_paths)
    assert all_paths == [(B, A, object)]


def test_mixedin_traverse_base_classes():
    class A:
        pass

    class B(A):
        pass

    class MixedIn:
        pass

    class C(MixedIn, B):
        pass

    all_paths = []
    traverse_base_classes(cls=C, all_paths=all_paths)
    assert all_paths == [(C, MixedIn, object), (C, B, A, object)]
