__package__ = 'plugins_extractor.wget'

from pathlib import Path

from pydantic_pkgr import BinName

from abx.archivebox.base_extractor import BaseExtractor, ExtractorName

from .binaries import WGET_BINARY
from .wget_util import wget_output_path

class WgetExtractor(BaseExtractor):
    name: ExtractorName = 'wget'
    binary: BinName = WGET_BINARY.name

    def get_output_path(self, snapshot) -> Path | None:
        wget_index_path = wget_output_path(snapshot.as_link())
        if wget_index_path:
            return Path(wget_index_path)
        return None

WGET_EXTRACTOR = WgetExtractor()


class WarcExtractor(BaseExtractor):
    name: ExtractorName = 'warc'
    binary: BinName = WGET_BINARY.name

    def get_output_path(self, snapshot) -> Path | None:
        warc_files = list((Path(snapshot.link_dir) / 'warc').glob('*.warc.gz'))
        if warc_files:
            return sorted(warc_files, key=lambda x: x.stat().st_size, reverse=True)[0]
        return None


WARC_EXTRACTOR = WarcExtractor()

