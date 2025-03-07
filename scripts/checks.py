import sys
import typing as t

import wom


def should_include_module(module: str) -> bool:
    return module != "annotations" and module[0] != "_" and module[0].upper() != module[0]


def get_modules() -> t.List[str]:
    return [m for m in wom.__dict__ if should_include_module(m)]


def get_alls() -> t.Tuple[t.Set[str], t.Set[str]]:
    modules = get_modules()
    return (
        set(item for module in modules for item in wom.__dict__[module].__all__),
        set(i for i in wom.__all__ if i not in modules),
    )


def validate_alls() -> bool:
    modules, lib = get_alls()
    err = None

    if missing := modules - lib:
        err = "Missing exported items at top level:\n" + "\n".join(f" - {m}" for m in missing)
        print(err, file=sys.stderr)

    if missing := lib - modules:
        err = "Missing exported items at module level:\n" + "\n".join(f" - {m}" for m in missing)
        print(err, file=sys.stderr)

    if err:
        return False

    return True


def validate_enums() -> bool:
    classes, _ = get_alls()
    missing: list[str] = []

    for c in classes:
        obj = wom.__dict__[c]

        try:
            skip = obj == wom.BaseEnum
            is_subclass = issubclass(obj, wom.BaseEnum)
            has_unknown = hasattr(obj, "Unknown")

            if not skip and is_subclass and not has_unknown:
                missing.append(c)
        except Exception:
            pass

    if missing:
        err = "Enums missing 'Unknown' variant:\n" + "\n".join(f" - {c}" for c in missing)
        print(err, file=sys.stderr)
        return False

    return True


if __name__ == "__main__":
    alls = validate_alls()
    enums = validate_enums()

    if not alls or not enums:
        sys.exit(1)
