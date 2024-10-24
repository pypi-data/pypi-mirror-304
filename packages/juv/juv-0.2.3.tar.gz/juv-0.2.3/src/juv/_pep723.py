import re

REGEX = r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"


def parse_inline_script_metadata(script: str) -> str | None:
    """Parse PEP 723 metadata from an inline script"""
    name = "script"
    matches = list(
        filter(lambda m: m.group("type") == name, re.finditer(REGEX, script))
    )
    if len(matches) > 1:
        raise ValueError(f"Multiple {name} blocks found")
    elif len(matches) == 1:
        content = "".join(
            line[2:] if line.startswith("# ") else line[1:]
            for line in matches[0].group("content").splitlines(keepends=True)
        )
        return content
    else:
        return None


def extract_inline_meta(script: str) -> tuple[str | None, str]:
    """Extract PEP 723 metadata from an inline script

    Parameters
    ----------
    script : str
        A Python script that may contain a PEP 723 metadata block

    Returns
    -------
    tuple[str | None, str]
        The extracted metadata block and the script with the metadata block removed
    """
    if match := re.search(REGEX, script):
        meta_comment = match.group(0)
        return meta_comment, script.replace(meta_comment, "").strip()
    return None, script


def includes_inline_metadata(script: str) -> bool:
    return re.search(REGEX, script) is not None
