from unittest.mock import MagicMock, patch

from hellbox.jobs.subset import Subset
from hellbox.jobs.subset.subset import _parse_unicodes


class TestParseUnicodes:
    def test_single(self):
        assert _parse_unicodes(["U+0041"]) == [0x0041]

    def test_range(self):
        assert _parse_unicodes(["U+0041-U+0043"]) == [0x0041, 0x0042, 0x0043]

    def test_multiple(self):
        assert _parse_unicodes(["U+0041", "U+0043"]) == [0x0041, 0x0043]


class TestSubset:
    def test_init(self):
        assert Subset("U+0000-U+007F")

    def test_init_with_glyphs(self):
        s = Subset("U+0041", glyphs=["space"])
        assert s.glyphs == ["space"]

    def test_process(self):
        file = MagicMock()
        copy = MagicMock()
        file.copy.return_value = copy

        with patch("hellbox.jobs.subset.subset.ft_subset") as mock_subset:
            mock_font = MagicMock()
            mock_subsetter = MagicMock()
            mock_subset.Options.return_value = MagicMock()
            mock_subset.load_font.return_value = mock_font
            mock_subset.Subsetter.return_value = mock_subsetter

            result = Subset("U+0041-U+0042").process(file)

        mock_subsetter.populate.assert_called_once_with(
            unicodes=[0x0041, 0x0042], glyphs=[]
        )
        mock_subsetter.subset.assert_called_once_with(mock_font)
        mock_subset.save_font.assert_called_once()
        assert result is copy
