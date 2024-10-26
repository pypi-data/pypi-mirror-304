"""
This is subtly different in places from the original groovy tokenizer,
which was intentionally structured similar to the original java implementation.
Though this is unpythonic in structure, it does make comparisons to the original
groovy tokenizer from j-concodese easier.
"""

from __future__ import annotations
import logging
import os
import hashlib
from pathlib import Path, PosixPath
from tree_sitter import Language, Parser
import tree_sitter_c as ts_c
import tree_sitter_cpp as ts_cpp
import tree_sitter_c_sharp as ts_c_sharp
import tree_sitter_java as ts_java
import tree_sitter_php as ts_php
import tree_sitter_rust as ts_rust
from .parsed_file import ParsedFile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TreeSitterParser:
    """
    base class for parsers that use tree sitter
    sub classes should implement a 'process_node' function
    """

    def __init__(self, language, extension) -> None:
        """
        language - str that matches tree sitter language grammar folder
        extension - str or tuple of file extensions this tokenizer will parse
        """
        self.md5 = hashlib.md5()
        self.extension = extension

        assert self.extension is not None
        language = Language(self.get_language_parser_from_language_str(language))
        self.parser = Parser(language)

    def get_language_parser_from_language_str(self, language):
        match language:
            case "c_sharp":
                return ts_c_sharp.language()
            case "cpp":
                return ts_cpp.language()
            case "c":
                return ts_c.language()
            case "rust":
                return ts_rust.language()
            case "php":
                return ts_php.language_php()
            case "java":
                return ts_java.language()
            case _:
                raise Exception(f"Parser not found for : '{language}'")

    def perform_extraction(self, project_path) -> list[ParsedFile]:
        """accept a single project path (dir) and processes all files in subfolders

        returns a list of ParsedFile instances"""
        paths_to_process = []
        paths_to_process += TreeSitterParser.list_files_for_folder(
            project_path, self.extension
        )

        parsed_files = []
        for idx, path_to_process in enumerate(paths_to_process):
            if (idx + 1) % 100 == 0:
                logger.info(f"parsing files {idx + 1}/{len(paths_to_process)}")

            parsed_files.append(
                self.parse_file_content(
                    path_to_process, self.get_relative_path(project_path, path_to_process)
                )
            )

        return parsed_files

    def get_relative_path(self, path_head_part, path_tail_part):
        head = Path(path_head_part)
        tail = Path(path_tail_part)

        head_components_length = len(head.parts)
        # tail_minus_head = Path(os.sep, *tail.parts[head_components_length:])
        tail_minus_head = Path(*tail.parts[head_components_length:])
        return str(tail_minus_head)

    def process_node(self, node, parsed_file, src_lines) -> None:
        raise NotImplementedError

    def parse_file_content(self, full_file_path, relative_path) -> ParsedFile:
        """parse a single src file and return a ParsedFile instance"""
        parsed_file = ParsedFile(
            file_name=Path(full_file_path).stem,
            extension=Path(full_file_path).suffix,
            relative_file_path=relative_path,
        )

        with open(full_file_path, "rb") as f:
            file_txt = f.read()
            self._set_md5_hash(file_txt, parsed_file)

            src_lines = file_txt.splitlines()

            file_txt = b"\n".join(src_lines)

            tree = self.parser.parse(file_txt)
            tree_cursor = tree.walk()

            fully_parsed = False

            while not fully_parsed:
                # process each new node on arrival
                self.process_node(tree_cursor.node, parsed_file, src_lines)
                # try to get to child node
                if tree_cursor.goto_first_child():
                    continue
                # if no children go to next sibling, or move up tree until a sibling
                # is found
                while not tree_cursor.goto_next_sibling():
                    if not tree_cursor.goto_parent():
                        fully_parsed = True  # no remaining unprocessed nodes
                        break

        return parsed_file

    def _set_md5_hash(self, file_txt, parsed_file):
        self.md5.update(file_txt)
        parsed_file.md5 = self.md5.hexdigest()

    def get_identifier_from_child(self, node, src_lines, child_type):
        """returns single matching identifier"""
        for child in node.children:
            if child.type == child_type:
                return self.process_substring(
                    src_lines, child.start_point, child.end_point
                )

    def process_substring(self, src_lines, start_point, end_point) -> str:
        """returns a string from the file currently in processing
        start and end point follow the same format as the properties
        of tree sitter nodes of the same name.
        tuple(line_number,column_number)  (0 based indexes)
        """
        # assert an error if identifiers are ever split across lines
        line_idx = start_point[0]
        final_line_idx = end_point[0]

        substring = ""
        # start by adding all the complete lines into one string
        while line_idx < final_line_idx:
            # new line characters are removed but we want to ensure that lines
            # have at least a space between them.
            # decode each line individually in case of a decode error - then
            # the error will only affect a single line, not the whole string
            substring += self.try_decode(src_lines[line_idx])
            substring += " "
            line_idx += 1

        # add the final truncated line
        col_start = start_point[1]
        col_end = end_point[1]

        substring += self.try_decode(src_lines[line_idx][col_start:col_end])
        return substring

    @staticmethod
    def try_decode(byte_string) -> str:
        """decodes a byte string and returns the result.
        if string cannot be decoded, an error message is output
        and an empty string is returned
        """
        try:
            return byte_string.decode("utf-8")
        except UnicodeDecodeError:
            print(
                f"(result: attempting latin-1 decode) UTF-8 decode error occured on the line: {byte_string}"
            )
        try:
            return byte_string.decode("latin-1")
        except UnicodeDecodeError:
            print(
                f"(result: line skipped) latin-1 decode error occured on the line: {byte_string}"
            )
        return ""

    @staticmethod
    def list_files_for_folder(path, extension) -> list[str]:
        """
        return a list of file paths in all subdirectories of a path which
        have the given extension
        """
        paths_to_process = []

        for root, _, files in os.walk(path, topdown=False):
            for file_name in files:
                if file_name.endswith(extension):
                    paths_to_process.append(os.path.join(root, file_name))

        return paths_to_process
