from __future__ import annotations
import xml.etree.ElementTree as ET
import logging
import re
import json
from pathlib import Path
import time
import datetime

from py_concodese.tokenizers.intt import Intt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class_name_pattern = "([A-Z]{1}[a-zA-Z0-9_0-9]*)"

# (For Java) matches the intro to a stack trace up until the first " at " before package.module.class.method etc.
# (For C++) matches the intro to a stack trace up until the first " at " before package.module.class.method etc.
stack_intro_pattern = "!(ENTRY|MESSAGE|STACK).+?(?=!|\sat\s)"

# stack_pattern = "at ((?:(?:[\d\w]*\.)*[\d\w]*))\.([\d\w\$]*)\.([\d\w\$]*)\s*\((?:(?:([\d\w]*\.(java|groovy)):(\d*))|([\d\w\s]*))\)"
stack_pattern = "at [^java\.|^sun\.]([a-z]+\.)*([A-Z]{1}[a-zA-Z0-9_0-9]*)(\$[A-Za-z0-9]*)?\.([A-Za-z0-9\_]*)\((([A-Z]{1}[a-zA-Z0-9_0-9]*\.java)\:[\d+]*)?(Unknown Source)?(Native Method)?\)"


class BReport:
    """A class to hold a bug report"""

    def __init__(
        self, bug_id, summary, description, fixed_files, lucene_helper, inc_dup_terms, reporting_time, tokenize_bug_reports=False#=datetime.datetime.now()
    ) -> None:
        """
        Args:
            bug_id ([type])
            summary ([type])
            description ([type])
            fixed_files (list): list of files requiring changes to fix bug
            lucene_helper ([type])
            inc_dup_terms (bool): include duplicate terms in the token lists
        """
        self.tokenize_bug_reports = tokenize_bug_reports
        self.intt = Intt()

        self.bug_id = bug_id

        # dictionaries initialised have two keys: False, True
        # these bools refer to the stemmed state of the tokens
        # bool -> []

        # words from the summary in certain positions
        self._key_position_words = {}
        self.set_key_position_words(summary, lucene_helper)

        # extract stack trace class names from the description if present
        self._stack_trace_classes = {}
        self.set_st_classes(description, lucene_helper)

        # if stack trace was found, remove it from desc
        # JAVA CONCODESE DOES NOT REMOVE STACK TRACE FROM DESC TOKENS
        # if len(self._stack_trace_classes[False]) > 0:
        #     description = re.sub(stack_intro_pattern, "", description)
        #     description = re.sub(stack_pattern, "", description)

        # tokens from summary and description
        self._summary_tokens = {}
        self._description_tokens = {}
        self._all_tokens = {}
        self.set_tokens(self._summary_tokens, summary, lucene_helper, inc_dup_terms)
        self.set_tokens(
            self._description_tokens, description, lucene_helper, inc_dup_terms
        )
        self.set_tokens(
            self._all_tokens, f"{summary} {description}", lucene_helper, inc_dup_terms
        )

        # files that were fixed in this BR
        self.fixed_files = fixed_files

        self.summary = summary
        self.description = description
        self.reporting_time = reporting_time

    def __str__(self) -> str:
        return str(
            (
                f"{self.bug_id if self.bug_id else ''}",
                f"summary={self.summary}",
                f"description={self.description}",
                f"fixed_files={self.fixed_files}",
                f"trace_classes={self._stack_trace_classes}",
                f"reporting_time={self.reporting_time}",
            )
        )

    def __eq__(self, other:BReport):
        return (other is not None and self.bug_id == other.bug_id and self.summary == other.summary
                and self.description == other.description and self.fixed_files == other.fixed_files
                and self._stack_trace_classes == other._stack_trace_classes)

    def __hash__(self) -> int:
        return hash(self.bug_id)


# "('89533', 'summary=[Themes] Colors and Fonts preferences page has funny icons for color entries', 'description=None', "fixed_files=['org.eclipse.swt.widgets.ImageList.java']", 'trace_classes={False: [], True: []}')"
    # {
    #    "closed_issues": {
    #         "1": {
    #             "issue_url": "https://github.com/catchorg/Catch2/issues/1845",
    #             "issue_id": "#1845",
    #             "issue_summary": "Assertion failed: !m_sectionStack.empty(), file catch.hpp line 5882",
    #             "issue_description": "schoetbi commented yesterday\nDescribe the bug\nWhile running the tests I got this assertion failure\nAssertion failed: !m_sectionStack.empty(), file D:\\GitlabRunner\\builds\\yz6XsHQZ\\0\\s\\catch\\catch.hpp, line 5882\nReproduction steps\nI start my console application under Windows with the following command line:\nbin\\Debug\\RtLib.Test.exe -s -r junit -o test_debug.xml ~OpDeadlockPreventionPattern\nI can only reproduce this on the buildserver, it did not happen on my dev machine yet. On the buildserver the tests runs within powershell (started by gitlab ci pipeline). But when I start this test through powershell on my dev machine the error did not occour.\nPlatform information:\nCompiler+version: MSVC v140\nCatch version: Catch v2.10.2 2019-10-24 17:49:11.459934",
    #             "issue_status": "Closed",
    #             "issue_reporting_time": "2020-01-27T11:54:18Z",
    #             "fixed_by": "",
    #             "pull_request_summary": "",
    #             "pull_request_description": "",
    #             "pull_request_status": "",
    #             "issue_fixed_time": "",
    #             "files_changed": []
    #         },
    #         "2": {
    #             "issue_url": "https://github.com/catchorg/Catch2/issues/1841",
    #             "issue_id": "#1841",
    #             "issue_summary": "Is it possible to force CHECK to behave like REQUIRES?",
    #             "issue_description": "dbak-invn commented 4 days ago\nIs there some compiler flag I can set to force CHECK to behave like REQUIRES?",
    #             "issue_status": "Closed",
    #             "issue_reporting_time": "2020-01-24T20:09:12Z",
    #             "fixed_by": "",
    #             "pull_request_summary": "",
    #             "pull_request_description": "",
    #             "pull_request_status": "",
    #             "issue_fixed_time": "",
    #             "files_changed": []
    #         },
    def to_json_for_file_storage(self):
        return {"issue_summary": self.summary,
                 "issue_description": self.description,
                 "files_changed":[self.fixed_files],
                 "trace_classes":self._stack_trace_classes,
                 "issue_id": self.bug_id,
                 }



    def get_kp_words(self, stemmed) -> list[str]:
        return self._key_position_words[stemmed]
        # return self.get_intt_tokenized_list_if_applicable(self._key_position_words[stemmed])

    def set_key_position_words(self, summary, lucene_helper) -> list[str]:
        """Uses the untokenized summary words to set the key position words used in lexical scoring
        src/main/java/de/dilshener/concodese/term/search/impl/ConceptPrecisionSearchImpl.java
        The list is assigned in the order: first, second, penult, final.
        """
        # split on common punctuation and spaces (but not full stop)
        summary_words = re.split("\-|,|\!|\?| ", summary)
        # filter out any 'words' that don't contain any letters
        filter_object = filter(lambda x: re.search("\w", x), summary_words)
        summary_words = list(filter_object)

        regex_class_name = BReport.compile_class_name_regex()

        key_position_words = []
        if len(summary_words) > 0:
            key_position_words.append(
                BReport.extract_class_name(summary_words[0], regex_class_name)
            )

        if len(summary_words) > 1:
            key_position_words.append(
                BReport.extract_class_name(summary_words[1], regex_class_name)
            )
            key_position_words.append(
                BReport.extract_class_name(summary_words[-2], regex_class_name)
            )
            key_position_words.append(
                BReport.extract_class_name(summary_words[-1], regex_class_name)
            )

        # lower case and strip out any leading or trailing full stops
        # (other punctuation will have been removed earlier)
        key_position_words = [word.lower().strip(".") for word in key_position_words]
        key_position_words = [word.lower() for word in key_position_words]

        self._key_position_words[False] = key_position_words
        self._key_position_words[True] = lucene_helper.stem_tokens(key_position_words)

    def get_st_classes(self, stemmed) -> list[str]:
        return self._stack_trace_classes[stemmed]
        # return self.get_intt_tokenized_list_if_applicable(self._stack_trace_classes[stemmed])

    def set_st_classes(self, description, lucene_helper):
        """extracts and stores the first 4 class names from the stack trace
        which aren't in the standard libraries"""
        class_names = []

        reg_stack = re.compile(stack_pattern)
        reg_class_name = re.compile(class_name_pattern)
        matches = reg_stack.finditer(description)
        for m in matches:
            str_containing_class = m.group(0)

            if not str_containing_class.startswith(
                ("at java.", "at sun.", "at groovy.")
            ):
                class_name = reg_class_name.search(str_containing_class).group(0)

                # order is important so can't use set
                if class_name not in class_names:
                    class_names.append(class_name)

            # only score the first 4
            if len(class_names) >= 4:
                break

        class_names = [class_name.lower() for class_name in class_names]
        self._stack_trace_classes[False] = class_names
        self._stack_trace_classes[True] = lucene_helper.stem_tokens(class_names)

    def get_summary_tokens(self, stemmed) -> list[str]:
        """returns an alphabetically sorted list of tokens"""
        return self._summary_tokens[stemmed]

    def get_description_tokens(self, stemmed) -> list[str]:
        """returns an alphabetically sorted list of tokens"""
        return self._description_tokens[stemmed]

    def get_all_tokens(self, stemmed) -> list[str]:
        """returns an alphabetically sorted list of tokens"""
        # return self._all_tokens[stemmed]
        return self.get_intt_tokenized_list_if_applicable(self._all_tokens[stemmed])

    def get_intt_tokenized_list_if_applicable(self, tokens):
        if self.tokenize_bug_reports:
            intt_tokenized_terms = []
            for term in tokens:
                intt_tokenized_terms.extend(self.intt.tokenize(term))

            tokens = intt_tokenized_terms
        return tokens

    def set_tokens(self, dict_, text, lucene_helper, include_duplicates):
        """adds stemmed and unstemmed tokens from the text to the dict
        See:
        src/main/java/de/dilshener/concodese/term/extract/impl/
        ChangeRequestCSVExtractorImpl.java

        In the original, a TreeSet object is used to store words, which
        is ordered:

        "according to the natural ordering of its elements.
        All elements inserted into the set must implement the Comparable
        interface."
        """
        # get tokens from text string
        tokens = lucene_helper.tokenize_string(text)
        lower_tokens = [token.lower() for token in tokens]

        # if self.tokenize_bug_reports:
        #     intt_tokenized_terms = []
        #     for term in lower_tokens:
        #         intt_tokenized_terms.extend(self.intt.tokenize(term))
        #
        #     lower_tokens = intt_tokenized_terms

        if not include_duplicates:
            # remove duplicates but keep as list type
            lower_tokens = list(set(lower_tokens))

        # sort for consistent order
        lower_tokens.sort()

        dict_[False] = lower_tokens
        # if two tokens have the same stem, the stemmed list will
        # include duplicates even if include_duplicates is False
        dict_[True] = lucene_helper.stem_tokens(lower_tokens)

    @staticmethod
    def compile_class_name_regex():
        return re.compile(class_name_pattern)

    @staticmethod
    def extract_class_name(word, reg_class_name):
        """extracts a class name or returns the original string"""
        matches = reg_class_name.finditer(word)
        for match in matches:
            return match.group()
        return word


def parse_bug_repository(
    file_path, lucene_helper, inc_dup_terms, max_size=None, tokenize_bug_reports=False
) -> list[BReport]:
    """parses a bug repository

    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Raises:
        ValueError: if file extension is not valid

    Returns:
        list[BReport]:
    """

    logger.info("Reading bug repository file")

    ext = Path(file_path).suffix.lower()

    if ext == ".xml":
        bug_reports = parse_xml_bug_repository(
            file_path, lucene_helper, inc_dup_terms, max_size=max_size, tokenize_bug_reports=tokenize_bug_reports
        )
    elif ext == ".json":
        bug_reports = parse_json_bug_repository(
            file_path, lucene_helper, inc_dup_terms, max_size=max_size, tokenize_bug_reports=tokenize_bug_reports
        )
    else:
        raise ValueError(
            "Invalid bug repository file type. Must be xml, or json and have a matching file extension."
        )

    logger.info(f"{len(bug_reports)} valid bug reports found")

    return bug_reports


def parse_xml_bug_repository(
    file_path, lucene_helper, inc_dup_terms, max_size=None, tokenize_bug_reports=False
) -> list[BReport]:
    """parses an xml bug repository
    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Returns:
        list[BReport]:
    """
    tree = ET.parse(file_path)

    bug_reports = []

    for child in tree.getroot():
        if max_size is not None and len(bug_reports) == max_size:
            break

        summary = child.find("buginformation").find("summary").text
        description = child.find("buginformation").find("description").text
        fixed_files = [f.text for f in child.find("fixedFiles").findall("file")]
        bug_reporting_time = child.attrib["opendate"]

        start = time.time()
        br = BReport(
            bug_id=child.attrib["id"],
            summary=summary if summary is not None else "",
            description=description if description is not None else "",
            fixed_files=fixed_files if len(fixed_files) > 0 else [],
            lucene_helper=lucene_helper,
            inc_dup_terms=inc_dup_terms,
            reporting_time=bug_reporting_time,
            tokenize_bug_reports=tokenize_bug_reports
        )
        end = time.time()
        print(f"Bug report {br.bug_id} parsed in: {end - start} seconds")
        bug_reports.append(br)

    return bug_reports


def parse_json_bug_repository(
    file_path,
    lucene_helper,
    inc_dup_terms,
    max_size=None,
    tokenize_bug_reports=False
) -> list[BReport]:
    """parses a json bug repository
    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Returns:
        list[BReport]:
    """
    ff_ext = (".c", ".cpp", ".rs", ".php", ".cs")

    # with open(file_path) as f:
    with open(file_path, encoding='utf8') as f:
        item = json.load(f)

    bug_reports = []
    value = []
    uselessbugs = 0
    usefulbugs = 0

    print(f"Total closed issues found: {len(item['closed_issues'].items())}")

    for issue_id, closed_issue in item["closed_issues"].items():
        if max_size is not None and len(bug_reports) == max_size:
            break

        value = closed_issue.get("files_changed", [])
        if value == []:
            uselessbugs = uselessbugs + 1
            continue

        summary = closed_issue["issue_summary"].strip().replace('\n', '')
        description = closed_issue["issue_description"].strip().replace('\n', '')

        # we are aware of two datastructures used,
        # 1. a list of two items [#id, file]
        # 2. a list of four items [#id, file, \u2192, file]
        # (there is sometimes repetition of files)
        fixed_files = set()
        for data in closed_issue["files_changed"]:
            for item in data:
                if "." in item:
                    fixed_files.add(item)

        if len(ff_ext) > 0 and not any(
            [fixed_file.endswith(ff_ext) for fixed_file in fixed_files]
        ):
            uselessbugs = uselessbugs + 1
            continue

        usefulbugs = usefulbugs + 1
        bug_id_withhash = closed_issue["issue_id"]
        # bug_id_withhash = issue_id
        bug_reporting_time = closed_issue["issue_reporting_time"]

        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T{0,1}\s{0,1}\d{2}:\d{2}:\d{2}Z{0,1}', bug_reporting_time):
            bug_reporting_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        br = BReport(
            bug_id=bug_id_withhash.replace("#", ""),
            summary=summary if summary is not None else "",
            description=description if description is not None else "",
            fixed_files=list(fixed_files) if len(fixed_files) > 0 else [],
            lucene_helper=lucene_helper,
            inc_dup_terms=inc_dup_terms,
            reporting_time=bug_reporting_time,
            tokenize_bug_reports=tokenize_bug_reports
        )
        bug_reports.append(br)

    # print("Total number of usable bugs:", uselessbugs)
    # print("Total number of unusable bugs:", usefulbugs)
    print(f"Total valid bug reports found: {len(bug_reports)}")
    return bug_reports

def parse_json_bug_repository_alternative(
    file_path,
    lucene_helper,
    inc_dup_terms,
    max_size=None,
) -> list[BReport]:
    """parses a json bug repository
    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Returns:
        list[BReport]:
    """
    # ff_ext = (".c", ".cpp", ".rs", ".java")
    ff_ext = (".java")

    with open(file_path) as f:
        data = json.load(f)

    bug_reports = []
    value = []
    uselessbugs = 0
    usefulbugs = 0

    for closed_issue in data:
        if max_size is not None and len(bug_reports) == max_size:
            break

        value = closed_issue["files"]
        if value == []:
            uselessbugs = uselessbugs + 1
            continue

        summary = closed_issue["summary"]
        description = closed_issue["description"]

        # we are aware of two datastructures used,
        # 1. a list of two items [#id, file]
        # 2. a list of four items [#id, file, \u2192, file]
        # (there is sometimes repetition of files)
        fixed_files = set()
        for item in closed_issue["files"]:
            fixed_files.add(item)

        if len(ff_ext) > 0 and not any([fixed_file.endswith(ff_ext) for fixed_file in fixed_files]):
            uselessbugs = uselessbugs + 1
            continue

        usefulbugs = usefulbugs + 1
        bug_id = closed_issue["bugId"]
        bug_reporting_time = closed_issue["reportTime"]

        br = BReport(
            bug_id=bug_id,
            summary=summary if summary is not None else "",
            description=description if description is not None else "",
            fixed_files=list(fixed_files) if len(fixed_files) > 0 else [],
            lucene_helper=lucene_helper,
            inc_dup_terms=inc_dup_terms,
            reporting_time=bug_reporting_time,
        )
        bug_reports.append(br)

    print("Total number of usable bugs:", usefulbugs)
    print("Total number of unusable bugs:", uselessbugs)
    return bug_reports

