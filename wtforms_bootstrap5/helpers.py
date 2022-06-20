import typing


def _traverse_base_classes(
    cls: typing.Type,
    all_paths: typing.List[typing.Tuple],
    current_path: typing.Tuple = tuple(),
):
    if cls is object:
        all_paths.append(current_path)
        return
    for base_class in cls.__bases__:
        _traverse_base_classes(
            cls=base_class,
            all_paths=all_paths,
            current_path=current_path + (cls,),
        )


def traverse_base_classes(cls: typing.Type) -> typing.List[typing.Tuple]:
    """Traverse all possible base classes paths to reach object.

    :param cls: the class to traverse
    :returns: a list of all possible paths to reach object from the given class
    """
    all_paths = []
    _traverse_base_classes(
        cls=cls,
        all_paths=all_paths,
    )
    return all_paths
