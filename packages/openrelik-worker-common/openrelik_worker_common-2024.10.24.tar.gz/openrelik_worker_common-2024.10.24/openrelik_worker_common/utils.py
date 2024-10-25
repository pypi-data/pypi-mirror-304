# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations  # support forward looking type hints

import base64
import fnmatch
import json
import os
import subprocess
import tempfile
from pathlib import Path, PurePath
from typing import Optional
from uuid import uuid4


def dict_to_b64_string(dict_to_encode: dict) -> str:
    """Encode a dictionary to a base64-encoded string.

    Args:
        dict_to_encode: The dictionary to encode.

    Returns:
        The base64-encoded string.
    """
    json_string = json.dumps(dict_to_encode)
    return base64.b64encode(json_string.encode("utf-8")).decode("utf-8")


def count_lines_in_file(file_path):
    """Count the number of lines in a file.

    Args:
        file_path: The path to the file.

    Returns:
        The number of lines in the file.
    """
    wc = subprocess.check_output(["wc", "-l", file_path])
    return int(wc.decode("utf-8").split()[0])


def get_input_files(pipe_result: str, input_files: list, filter: dict = None) -> list:
    """Set the input files for the task.

    Args:
        pipe_result: The result of the previous task (from Celery).
        input_files: The input files for the task.

    Returns:
        The input files for the task.
    """
    if pipe_result:
        result_string = base64.b64decode(pipe_result.encode("utf-8")).decode("utf-8")
        result_dict = json.loads(result_string)
        input_files = result_dict.get("output_files")

    if filter:
        input_files = filter_compatible_files(input_files, filter)

    return input_files


def task_result(
    output_files: list,
    workflow_id: str,
    command: str = None,
    meta: dict = None,
    file_reports: list = [],
    task_report: dict = None,
) -> str:
    """Create a task result dictionary and encode it to a base64 string.

    Args:
        output_files: List of output file dictionaries.
        workflow_id: ID of the workflow.
        command: The command used to execute the task.
        meta: Additional metadata for the task (optional).
        file_reports: List of file report dictionaries.
        task_report: A dictionary representing a task report.

    Returns:
        Base64-encoded string representing the task result.
    """
    result = {
        "output_files": output_files,
        "workflow_id": workflow_id,
        "command": command,
        "meta": meta,
        "file_reports": file_reports,
        "task_report": task_report,
    }
    return dict_to_b64_string(result)


def create_file_report(
    input_file: dict,
    report_file: OutputFile,
    report: object,
) -> str:
    """Create a file report dictionary.

    Args:

    Returns:
    """
    return {
        "summary": report.summary,
        "priority": report.priority,
        "input_file_uuid": input_file.get("uuid"),
        "content_file_uuid": report_file.uuid,
    }


class OutputFile:
    """Represents an output file.

    Attributes:
        uuid: Unique identifier for the file.
        display_name: Display name for the file.
        extension: Extension of the file.
        data_type: Data type of the file.
        path: The full path to the file.
        original_path: The full original path to the file.
        source_file_id: The OutputFile this file belongs to.
    """

    def __init__(
        self,
        uuid: str,
        output_path: str,
        display_name: str,
        extension: Optional[str] = None,
        data_type: Optional[str] = None,
        original_path: Optional[str] = None,
        source_file_id: Optional[OutputFile] = None,
    ):
        """Initialize an OutputFile object.

        Args:
            uuid: Unique identifier (uuid4) for the file.
            output_path: The path to the output directory.
            display_name: The name of the output file.
            extension: File extension (optional).
            data_type: The data type of the output file (optional).
            orignal_path: The orignal path of the file (optional).
            source_file_id: The OutputFile this file belongs to (optional).
        """
        self.uuid = uuid
        self.display_name = display_name
        self.extension = extension
        self.data_type = data_type
        self.path = output_path
        self.original_path = original_path
        self.source_file_id = source_file_id

    def to_dict(self):
        """
        Return a dictionary representation of the OutputFile object.
        This is what the mediator server gets and uses to create a File in the database.

        Returns:
            A dictionary containing the attributes of the OutputFile object.
        """
        return {
            "uuid": self.uuid,
            "display_name": self.display_name,
            "extension": self.extension,
            "data_type": self.data_type,
            "path": self.path,
            "original_path": self.original_path,
            "source_file_id": self.source_file_id,
        }


def create_output_file(
    output_base_path: str,
    display_name: Optional[str] = None,
    extension: Optional[str] = None,
    data_type: Optional[str] = None,
    original_path: Optional[str] = None,
    source_file_id: Optional[OutputFile] = None,
) -> OutputFile:
    """Creates and returns an OutputFile object.

    Args:
        output_base_path: The path to the output directory.
        display_name: The name of the output file (optional).
        extension: File extension (optional).
        data_type: The data type of the output file (optional).
        original_path: The orignal path of the file (optional).
        source_file_id: The OutputFile this file belongs to (optional).

    Returns:
        An OutputFile object.
    """
    # Create a new UUID for the file to use as filename on disk.
    uuid = uuid4().hex

    # If display_name is missing, set the file's UUID as display_name.
    display_name = display_name if display_name else uuid

    # Allow for an explicit extension to be set.
    if extension:
        extension = extension.lstrip(".")
        display_name = f"{display_name}.{extension}"

    # Extract extension from filename if present
    _, extracted_extension = os.path.splitext(display_name)

    # Construct the full output path.
    output_filename = f"{uuid}{extracted_extension}"
    output_path = os.path.join(output_base_path, output_filename)

    return OutputFile(
        uuid=uuid,
        output_path=output_path,
        display_name=display_name,
        extension=extracted_extension,
        data_type=data_type,
        original_path=original_path,
        source_file_id=source_file_id,
    )


def get_path_without_root(path: str) -> str:
    """Converts a full path to relative path without the root.

    Args:
        path: A full path.

    Returns:
        A relative path without the root.
    """
    path = PurePath(path)
    return str(path.relative_to(path.anchor))


def build_file_tree(
    output_path: str, files: list[OutputFile]
) -> tempfile.TemporaryDirectory | None:
    """Creates the original file tree structure from a list of OutputFiles.

    Args:
        output_path: Path to the OpenRelik output directory.
        files: A list of OutPutFile instances.

    Returns:
        The root path of the file tree as a TemporaryDirectory or None.
    """
    if not files or not all(isinstance(file, OutputFile) for file in files):
        return None

    tree_root = tempfile.TemporaryDirectory(dir=output_path, delete=False)

    for file in files:
        normalized_path = os.path.normpath(file.original_path)
        original_filename = Path(normalized_path).name
        original_folder = Path(normalized_path).parent
        relative_original_folder = get_path_without_root(original_folder)
        # Create complete folder structure.
        try:
            tmp_full_path = os.path.join(tree_root.name, relative_original_folder)

            # Ensure that the constructed path is within the system's temporary
            # directory, preventing attempts to write files outside of it.
            if tree_root.name not in tmp_full_path:
                raise PermissionError(
                    f"Folder {tmp_full_path} not in OpenRelik output_path: {output_path}"
                )

            os.makedirs(tmp_full_path)
        except FileExistsError:
            pass
        # Create hardlink to file.
        os.link(
            file.path,
            os.path.join(tree_root.name, relative_original_folder, original_filename),
        )

    return tree_root


def delete_file_tree(root_path: tempfile.TemporaryDirectory):
    """Delete a temporary file tree folder structure.

    Args:
        root_path: TemporaryDirectory root object of file tree structure.

    Returns: None
    Raises: TypeError
    """
    if not isinstance(root_path, tempfile.TemporaryDirectory):
        raise TypeError("Root path is not a TemporaryDirectory object!")

    root_path.cleanup()


def filter_compatible_files(input_files, filter_dict):
    """
    Filters a list of files based on compatibility with a given filter,
    including partial matching.

    Args:
      input_files: A list of file dictionaries, each containing keys
                   "data_type", "mime-type", "filename", and "extension".
      filter_dict: A dictionary specifying the filter criteria with keys
                   "data_types", "mime-types", and "extensions".

    Returns:
      A list of compatible file dictionaries.
    """
    compatible_files = []
    for file_data in input_files:
        if file_data.get("data_type") is not None and any(
            fnmatch.fnmatch(file_data["data_type"], pattern)
            for pattern in filter_dict["data_types"]
        ):
            compatible_files.append(file_data)
        elif file_data.get("mime_type") is not None and any(
            fnmatch.fnmatch(file_data["mime_type"], pattern)
            for pattern in filter_dict["mime_types"]
        ):
            compatible_files.append(file_data)
        elif file_data.get("display_name") is not None and any(
            fnmatch.fnmatch(file_data["display_name"], pattern)
            for pattern in filter_dict["filenames"]
        ):
            compatible_files.append(file_data)
    return compatible_files
