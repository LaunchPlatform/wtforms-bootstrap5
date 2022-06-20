import typing


def traverse_base_classes(
    cls: typing.Type,
    all_paths: typing.List[typing.Tuple],
    current_path: typing.Tuple = tuple(),
):
    """Traverse all possible base classes paths to reach object.

    :param cls: the class to traverse
    :param all_paths: list for containing all possible paths to `object` class
    :param current_path: current path (used only for recursive call mostly)
    """
    if cls is object:
        all_paths.append(current_path + (cls,))
        return
    for base_class in cls.__bases__:
        traverse_base_classes(
            cls=base_class,
            all_paths=all_paths,
            current_path=current_path + (cls,),
        )
