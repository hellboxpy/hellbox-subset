from fontTools import subset as ft_subset

from hellbox import Chute, Hellbox


def _parse_unicodes(unicode_strs):
    codepoints = []
    for u in unicode_strs:
        u = u.strip()
        parts = u.split("-")
        if len(parts) == 2 and parts[1].upper().startswith("U+"):
            start = int(parts[0].upper().lstrip("U+"), 16)
            end = int(parts[1].upper().lstrip("U+"), 16)
            codepoints.extend(range(start, end + 1))
        else:
            codepoints.append(int(u.upper().lstrip("U+"), 16))
    return codepoints


class Subset(Chute):
    """Subset removes glyphs from a font not covered by the given unicode
    ranges or glyph names."""

    def __init__(self, *unicodes, glyphs=()):
        self.unicodes = unicodes
        self.glyphs = list(glyphs)

    def process(self, file):
        Hellbox.info(f"Subsetting: {file.name}")
        copy = file.copy()
        options = ft_subset.Options()
        font = ft_subset.load_font(str(copy.content_path), options)
        subsetter = ft_subset.Subsetter(options=options)
        subsetter.populate(
            unicodes=_parse_unicodes(self.unicodes),
            glyphs=self.glyphs,
        )
        subsetter.subset(font)
        ft_subset.save_font(font, str(copy.content_path), options)
        return copy
