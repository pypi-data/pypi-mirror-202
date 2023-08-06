from audiobookdl import logging
from typing import Optional
from mutagen import File
import os

MIMETYPE_TO_EXTENSION = {
    "audio/mp3": "mp3",
    "audio/x-aac": "mp4",
}

EQUIVALENT_FORMATS = [
    ["aac", "mp4", "m4a", "m4b"]
]

def get_input_and_output_formats(option: Optional[str], files: list[str]) -> tuple[str, str]:
    """
    Get input and output formats for files

    `option` is used if specied; else it's based on the file extensions
    """
    current_format = _get_filetype(files)
    logging.debug(f"{current_format=}")
    output_format = _get_output_format(current_format, option)
    logging.debug(f"{output_format=}")
    for ef in EQUIVALENT_FORMATS:
        if current_format in ef and output_format in ef:
            current_format = output_format
    return current_format, output_format

def _get_filetype(files: list[str]) -> str:
    current_format = _get_filetype_from_content(files)
    if current_format is None:
        current_format = _get_filetype_from_extension(files)
    return current_format

def _get_filetype_from_content(files: list[str]) -> Optional[str]:
    mutagen_file = File(files[0])
    if mutagen_file is None:
        return None
    for mimetype in mutagen_file.mime:
        if mimetype in MIMETYPE_TO_EXTENSION:
            return MIMETYPE_TO_EXTENSION[mimetype]
    return None

def _get_filetype_from_extension(files: list[str]) -> str:
    first_file = files[0]
    extension = os.path.splitext(first_file)[1]
    return extension[1:] # Remiving '.' in extension

def _get_output_format(current_format: str, option: Optional[str]) -> str:
    if option:
        output_format = option
    elif current_format == "ts":
        output_format = "mp3"
    else:
        output_format = current_format
    return output_format
