"""
tools/downloader.py

Utilities for downloading datasets and files from URLs.
"""

from pathlib import Path
from urllib.parse import urlparse
import mimetypes
import tempfile
import zipfile

import requests

from services.logger import logger


class Downloader:
    """
    Download and manage remote files.
    """

    def __init__(self):
        self.download_dir = Path(tempfile.gettempdir()) / "telegram_data_bot"
        self.download_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Download File
    # ---------------------------------------------------------

    def download(self, url: str) -> Path:
        """
        Download a file and return its local path.
        """

        logger.log(
            "download_started",
            url=url
        )

        response = requests.get(
            url,
            timeout=60,
            stream=True
        )

        response.raise_for_status()

        filename = self._filename_from_url(url)

        path = self.download_dir / filename

        with open(path, "wb") as file:
            for chunk in response.iter_content(8192):
                if chunk:
                    file.write(chunk)

        logger.log(
            "download_completed",
            path=str(path),
            size=path.stat().st_size
        )

        return path

    # ---------------------------------------------------------
    # Detect File Type
    # ---------------------------------------------------------

    def file_type(self, path: Path) -> str:
        """
        Detect file type from extension.
        """

        suffix = path.suffix.lower()

        mapping = {
            ".csv": "csv",
            ".xlsx": "excel",
            ".xls": "excel",
            ".json": "json",
            ".html": "html",
            ".htm": "html",
            ".zip": "zip"
        }

        return mapping.get(suffix, "unknown")

    # ---------------------------------------------------------
    # Extract ZIP
    # ---------------------------------------------------------

    def extract_zip(self, path: Path) -> list[Path]:
        """
        Extract a ZIP archive.
        """

        output = self.download_dir / path.stem
        output.mkdir(exist_ok=True)

        with zipfile.ZipFile(path) as archive:
            archive.extractall(output)

        files = list(output.rglob("*"))

        logger.log(
            "zip_extracted",
            directory=str(output),
            files=len(files)
        )

        return files

    # ---------------------------------------------------------
    # Guess MIME Type
    # ---------------------------------------------------------

    def mime_type(self, path: Path) -> str:
        """
        Guess MIME type.
        """

        mime, _ = mimetypes.guess_type(path)

        return mime or "application/octet-stream"

    # ---------------------------------------------------------
    # Filename
    # ---------------------------------------------------------

    def _filename_from_url(self, url: str) -> str:
        """
        Extract filename from URL.
        """

        parsed = urlparse(url)

        filename = Path(parsed.path).name

        if filename:
            return filename

        return "downloaded_file"

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    def cleanup(self):
        """
        Remove downloaded files.
        """

        for file in self.download_dir.glob("*"):

            if file.is_file():
                file.unlink()


downloader = Downloader()
