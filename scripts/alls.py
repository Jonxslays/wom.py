import typing as t


def validate_alls() -> None:
    import wom

    should_include_module: t.Callable[[str], bool] = lambda m: (
        m != "annotations" and m[0] != "_" and m[0].upper() != m[0]
    )

    modules_all: set[str] = set()
    modules = [m for m in wom.__dict__ if should_include_module(m)]
    modules_all.update(item for module in modules for item in wom.__dict__[module].__all__)
    lib_all = set(i for i in wom.__all__ if i not in modules)

    if missing := modules_all.difference(lib_all):
        raise Exception(
            "Missing exported items at top level:\n" + "\n".join(f" - {m}" for m in missing)
        )

    if missing := lib_all.difference(modules_all):
        raise Exception(
            "Missing exported items at module level:\n" + "\n".join(f" - {m}" for m in missing)
        )


if __name__ == "__main__":
    validate_alls()
