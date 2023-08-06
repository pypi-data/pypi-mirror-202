from PyQt6.QtCore import QCoreApplication
import collections
import os

FLATPAK_DIRS = (
    "/var/lib/flatpak",
    os.path.expanduser("~/.local/share/flatpak"),
    "/tmp/testflatpak"
)

_compression_tuple = collections.namedtuple("compression_tuple", ("name", "mode", "suffix"))
COMPRESSION_METHODS = (
    _compression_tuple(QCoreApplication.translate("Constants", "None"), "w", ""),
    _compression_tuple("gzip", "w:gz", ".gz"),
    _compression_tuple("bzip2", "w:bz2", ".bz2"),
    _compression_tuple("LZMA", "w:xz", ".xz")
)

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"
