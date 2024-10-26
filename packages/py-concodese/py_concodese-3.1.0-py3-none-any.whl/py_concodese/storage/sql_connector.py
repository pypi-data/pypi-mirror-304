""" A module that handles database interaction """
from __future__ import annotations

from py_concodese.storage.modelless import modelless_factory
from .sql_base import initialise
from .models import File, Identifier, Token, CommentToken
from .modelless import File as modelless_file
from sqlalchemy import select
from jpype import JClass
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FileNotInDB(Exception):
    pass

class SqlConnector:
    def __init__(
        self,
        file_based,
        sqlite_dir,
        clean_db=False,
        test=False,
        project_id=None,
    ) -> None:
        """_summary_

        Args:
            file_based (bool): whether to create an sqlite file or an in-memory db
            sqlite_dir (str): path to directory to contain sqlite file
            clean_db (bool, optional): Deletes any existing db. Defaults to False.
            test (bool, optional): Is this instance part of an automated test. Defaults to False.
            project_id (int, optional): An id to identify a project with. Defaults to None.
        """
        # store some sql settings in the class
        self.file_based = file_based
        self.sqlite_dir = sqlite_dir
        self.test = test
        self.project_id = project_id

        self.files_batch = {}  # This temporarily stores file objects when scanning for tokens before translating comments

        # initialise connection with sqlite
        self.session = initialise(
            file_based,
            sqlite_dir,
            clean_db,
            test,
            project_id,
        )

    def clean_db(self):
        """deletes any existing database with matching parameters to this instance"""
        # close existing connection
        self.close()

        # reinitialise session and clean db
        self.session = initialise(
            self.file_based,
            self.sqlite_dir,
            clean_db=True,
            test=self.test,
            project_id=self.project_id,
        )

    def store_tokens(self, parsed_files, tokenizer_helper, intt) -> None:
        """ Former method used to store tokens without the translation layer
        The new method (scan_tokens) doesn't run the batch_tokenize_and_translate_file_comments which translates the comments
        This is so the full list of comments can be retrieved to the main.py file and so it can prompt the user for confirmation before translating

        """
        self.scan_tokens(parsed_files, tokenizer_helper, intt)
        self.batch_tokenize_and_translate_file_comments(self.get_untranslated_files_as_dict(parsed_files), tokenizer_helper, skip_translation=True)

        logger.info(f"All tokens created")


    def scan_tokens(self, parsed_files, tokenizer_helper, intt) -> None:
        """for each parsed file, stores identifiers, creates and stores tokens in db
        Args:
            parsed_files - list[ParsedFile]
            tokenizer_helper - instance of LuceneHelper/SpacyHelper
            intt - instance of intt
        """

        self.files_batch.clear()

        # initialise the file row
        for idx, parsed_file in enumerate(parsed_files):
            if (idx + 1) % 50 == 0:
                logger.info(
                    f"Creating and storing tokens from files {idx + 1}/{len(parsed_files)}"
                )
                # commit changes regularly so that we don't have a massive sql
                # write, and we can keep the user updated with progress more
                # accurately
                self.session.commit()

            file_row = self.add_file_to_session(tokenizer_helper, parsed_file)

            if file_row.is_translated:
                # If the file is translated, then skip adding identifiers and skip adding it to the list to batch translate
                continue

            # add file name as identifier
            identifier_row = self.add_identifier_to_session(tokenizer_helper, file_row, parsed_file.file_name)
            self.add_tokens_to_session(tokenizer_helper, intt.tokenize(parsed_file.file_name), identifier_row, file_row)

            # add each identifier
            for identifier_text in parsed_file.code_identifiers:
                identifier_row = self.add_identifier_to_session(
                    tokenizer_helper, file_row, identifier_text
                )

                # create tokens from the identifier
                tokens = intt.tokenize(identifier_text)
                self.add_tokens_to_session(
                    tokenizer_helper, tokens, identifier_row, file_row
                )
            # tokens = tokenizer_helper.tokenize_list(comment_strings)
            # stemmed_tokens = tokenizer_helper.stem_tokens(tokens)
            # for token, stemmed_token in zip(tokens, stemmed_tokens):
            #     self.session.add(CommentToken(file_row, token, stemmed_token))
            #
            # # add comments
            # self.add_comment_tokens_to_session(
            #     tokenizer_helper, file_row, parsed_file.comment_strings
            # )

            # Add file objects to a dictionary to batch tokenize below
            self.files_batch[parsed_file.relative_file_path] = file_row

        self.session.commit()
        logger.info(f"All identifier tokens created")

        # self.batch_tokenize_and_translate_file_comments(files_batch, parsed_files, tokenizer_helper)



    #
    #
    # def store_tokens(self, parsed_files, tokenizer_helper, intt) -> None:
    #     """for each parsed file, stores identifiers, creates and stores tokens in db
    #     Args:
    #         parsed_files - list[ParsedFile]
    #         tokenizer_helper - instance of LuceneHelper/SpacyHelper
    #         intt - instance of intt
    #     """
    #
    #     files_batch = {}
    #
    #     # initialise the file row
    #     for idx, parsed_file in enumerate(parsed_files):
    #         if (idx + 1) % 50 == 0:
    #             logger.info(
    #                 f"Creating and storing tokens from files {idx + 1}/{len(parsed_files)}"
    #             )
    #             # commit changes regularly so that we don't have a massive sql
    #             # write, and we can keep the user updated with progress more
    #             # accurately
    #             self.session.commit()
    #
    #         file_row = self.add_file_to_session(tokenizer_helper, parsed_file)
    #
    #         if file_row.is_translated:
    #             # If the file is translated, then skip adding identifiers and skip adding it to the list to batch translate
    #             continue
    #         # add each identifier
    #         for identifier_text in parsed_file.code_identifiers:
    #             identifier_row = self.add_identifier_to_session(
    #                 tokenizer_helper, file_row, identifier_text
    #             )
    #
    #             # create tokens from the identifier
    #             tokens = intt.tokenize(identifier_text)
    #             self.add_tokens_to_session(
    #                 tokenizer_helper, tokens, identifier_row, file_row
    #             )
    #         # tokens = tokenizer_helper.tokenize_list(comment_strings)
    #         # stemmed_tokens = tokenizer_helper.stem_tokens(tokens)
    #         # for token, stemmed_token in zip(tokens, stemmed_tokens):
    #         #     self.session.add(CommentToken(file_row, token, stemmed_token))
    #         #
    #         # # add comments
    #         # self.add_comment_tokens_to_session(
    #         #     tokenizer_helper, file_row, parsed_file.comment_strings
    #         # )
    #
    #         # Add file objects to a dictionary to batch tokenize below
    #         files_batch[parsed_file.relative_file_path] = file_row
    #
    #     self.batch_tokenize_and_translate_file_comments(files_batch, parsed_files, tokenizer_helper)
    #
    #     # final write for any changes
    #     self.session.commit()
    #
    #     logger.info(f"All tokens created")

    def batch_tokenize_and_translate_file_comments(self, filename_comments_dict, tokenizer_helper, skip_translation=False):
        #     filename_comments_dict = self.get_untranslated_files_as_dict(parsed_files)
        tokenized_files = []
        if len(filename_comments_dict) > 0 :
            tokenized_files = tokenizer_helper.tokenize_batch(filename_comments_dict, skip_translation=skip_translation, remove_stop_words=True)
        for tokenized_file in tokenized_files:
            for token in tokenized_file.tokens:
                file_object = self.files_batch[tokenized_file.full_path]
                self.session.add(CommentToken(file_object, token.plain_token, token.stemmed_token))
            # self.set_file_as_translated(tokenized_file.filename, tokenized_file.is_translated)
            self.set_file_as_translated(tokenized_file.full_path, tokenized_file.is_translated)
            self.session.commit()

    def get_untranslated_files_as_dict(self, parsed_files):
        # Query for old files from database
        # compare with the current list and see if they are equal and are translated or not
        # remove files from filename_comments_dict that don't need to be translated

        stored_files = self.get_src_files()

        stored_files_md5_and_translation_status = {file.relative_file_path: {'md5':file.md5, 'is_translated':file.is_translated, 'name': file.name} for file in stored_files}
        filename_comments_dict = {}

        for parsed_file in parsed_files:
            stored_file= stored_files_md5_and_translation_status[parsed_file.relative_file_path]
            # if not stored_file['is_translated'] or stored_file['md5'] != parsed_file.md5:
            #     # If file is already translated and comments are the same, skip translation by removing from dict
            #     del filename_comments_dict[stored_file.name]
            if not stored_file['is_translated'] or stored_file['md5'] != parsed_file.md5:
                # If file is already translated and comments are the same, skip translation by removing from dict
                filename_comments_dict[parsed_file.relative_file_path] = parsed_file.comment_strings
            del stored_files_md5_and_translation_status[parsed_file.relative_file_path]

        # TODO remove files still in stored_files_md5_and_translation_status because they don't exist anymore, except in the database

        # stored_files = self.get_src_files()
        # filename_comments_dict = {parsed_file.file_name: parsed_file.comment_strings for parsed_file in parsed_files}
        # for stored_file in stored_files:
        #     updated_file_comments = filename_comments_dict[stored_file.name]
        #     if stored_file.is_translated and stored_file.md5 == self.are_comments_equal(stored_file, updated_file_comments):
        #         # If file is already translated and comments are the same, skip translation by removing from dict
        #         del filename_comments_dict[stored_file.name]
        # return filename_comments_dict
        return filename_comments_dict

    def are_comments_equal(self, stored_file, updated_file_comments):
        return set(stored_file.comment_tokens) != set(updated_file_comments)

    def set_file_as_translated(self, full_path, is_translated: bool = True):
        self.session.query(File).filter(File.relative_file_path == full_path).update({'is_translated': is_translated})

    def close(self) -> None:
        """closes sessions"""
        self.session.close()

    def add_tokens_to_session(
        self,
        tokenizer_helper,
        tokens,
        identifier_row: Identifier,
        file_row: File,
    ) -> None:
        """_summary_

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            tokens (list[str]):
            identifier_row (Identifier):
            file_row (File):
        """
        stemmed_tokens = tokenizer_helper.stem_tokens(tokens)

        for token, stemmed_token in zip(tokens, stemmed_tokens):
            token_row = Token(identifier_row, token, stemmed_token, file_row)
            self.session.add(token_row)

    def add_file_to_session(self, tokenizer_helper, parsed_file) -> File:
        """adds a File object to the session

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            parsed_file (ParsedFile):

        Returns:
            File:
        """


        existing_file_in_db = self.session.query(File).filter(File.name == parsed_file.file_name,
                                      File.extension == parsed_file.extension,
                                      File.relative_file_path == parsed_file.relative_file_path
                                      ).first()
        if existing_file_in_db is None:

            file_row = File(
                name=parsed_file.file_name,
                stemmed_name=tokenizer_helper.stem_token(parsed_file.file_name),
                package=parsed_file.package,
                extension=parsed_file.extension,
                relative_file_path=parsed_file.relative_file_path,
                md5=parsed_file.md5,
                is_translated=False,
            )
            self.session.add(file_row)
            return file_row

        if existing_file_in_db.md5 is None or existing_file_in_db.md5 != parsed_file.md5:
            file_row = self.session.query(File).filter(File.name == parsed_file.file_name,
                                                       File.extension == parsed_file.extension,
                                                       File.relative_file_path == parsed_file.relative_file_path
                                                       ).update({'md5': parsed_file.md5, 'is_translated': False})
            return file_row
        else:
            # File exists and is already translated (is the same md5)
            return existing_file_in_db


        # existing_file_in_db = None
        # try:
        #     existing_file_in_db = self.session.query(File).filter(File.name == parsed_file.file_name,
        #                                   File.extension == parsed_file.extension,
        #                                   File.relative_file_path == parsed_file.relative_file_path
        #                                   ).first()
        #     if existing_file_in_db is None or existing_file_in_db.md5 is None or existing_file_in_db.md5 != parsed_file.md5:
        #         is_translated = False
        #     else:
        #         is_translated = True
        # except FileNotInDB:
        #     is_translated = False
        #
        #
        # if existing_file_in_db is not None and not is_translated:
        #     file_row = self.session.query(File).filter(File.name == parsed_file.file_name,
        #                                   File.extension == parsed_file.extension,
        #                                   File.relative_file_path == parsed_file.relative_file_path
        #                                   ).update({'md5': parsed_file.md5, 'is_translated': False})
        # else:
        #     file_row = File(
        #         name=parsed_file.file_name,
        #         stemmed_name=tokenizer_helper.stem_token(parsed_file.file_name),
        #         package=parsed_file.package,
        #         extension=parsed_file.extension,
        #         relative_file_path=parsed_file.relative_file_path,
        #         md5=parsed_file.md5,
        #         is_translated=is_translated,
        #     )
        #     self.session.add(file_row)
        #
        # return file_row

    def add_identifier_to_session(
        self,
        tokenizer_helper,
        file_row: File,
        identifier_text: str,
    ) -> Identifier:
        """adds an Identifier object to the session

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            file_row (File):
            identifier_text (str):

        Returns:
            Identifier:
        """
        stemmed_text = tokenizer_helper.stem_token(identifier_text)
        identifier_row = Identifier(file_row, identifier_text, stemmed_text)
        self.session.add(identifier_row)
        return identifier_row

    def add_comment_tokens_to_session(
        self, tokenizer_helper, file_row: File, comment_strings
    ) -> None:
        """Adds the tokens from comment strings db session

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            file_row (File):
            comment_strings (list[str]):
        """
        tokens = tokenizer_helper.tokenize_list(comment_strings)
        stemmed_tokens = tokenizer_helper.stem_tokens(tokens)
        for token, stemmed_token in zip(tokens, stemmed_tokens):
            self.session.add(CommentToken(file_row, token, stemmed_token))

    def get_src_files(
        self,
        modelless=True,
    ) -> list[modelless_file] | list[File]:
        """retrieves all src files from the db

        Args:
            modelless (bool, optional): Whether to return the db objects as a
            collection of modelless_file. Defaults to True.

        Returns:
            list[modelless_file]|list[File]:
        """
        db_src_files = self.session.query(File).all()
        if not modelless:
            return db_src_files

        logger.info("Optimising src file token data for in memory searches")
        src_files = []
        for idx, db_src_file in enumerate(db_src_files):
            if (idx + 1) % 100 == 0:
                logger.info(
                    f"Optimising src file token data for in memory searches {idx+1}/{len(db_src_files)}"
                )
            src_files.append(modelless_factory(db_src_file))
        logger.info("Optimisation complete")
        return src_files

    def get_src_file_by_name(self, name, stemmed) -> modelless_file:
        """gets the db data for a File with a matching name

        Args:
            name (_type_): name to be searched for
            stemmed (bool): whether to search the stemmed name field 

        Raises:
            Exception: if not file with that name is found

        Returns:
            modelless_file: the first matching File, converted to a modelless instance
        """
        if not stemmed:
            stmt = select(File).where(File.name == name)
        else:
            stmt = select(File).where(File.stemmed_name == name)

        for file_row in self.session.execute(stmt):
            # return first instance
            return modelless_factory(file_row._data[0])
        else:
            raise FileNotInDB("no file by that name found")

    def store_data_from_jim_derby(self, parsed_files, tokenizer_helper, db_dir):
        """extracts data from the derby database created by JIM
        and insert data into the sqlite format used by the rest of
        the application
        """

        # connect to db
        con_string = f"jdbc:derby:{db_dir};"
        sql_driver = JClass("java.sql.DriverManager").getConnection(con_string)

        # execute statement
        query_base = (
            "select file_name, identifier_name, component_word "
            "from SVM.files files join SVM.PROGRAM_ENTITIES "
            "pgm_ent on pgm_ent.file_name_key_fk = files.file_name_key "
            "join SVM.IDENTIFIER_NAMES idents on idents.identifier_name_key = "
            "pgm_ent.identifier_name_key_fk "
            "join SVM.COMPONENT_WORDS_XREFS xrefs on "
            "xrefs.identifier_name_key_fk = idents.identifier_name_key "
            "join SVM.COMPONENT_WORDS cws on cws.COMPONENT_word_key = "
            "xrefs.COMPONENT_word_key_fk "
            "WHERE SVM.files.file_name ="
        )
        query_order = "ORDER BY IDENTIFIER_NAME"

        # for each parsed src file
        for parsed_file in parsed_files:
            # add file to db session
            file_row = self.add_file_to_session(tokenizer_helper, parsed_file)

            # add comments from file
            self.add_comment_tokens_to_session(
                tokenizer_helper, file_row, parsed_file.comment_strings
            )

            # get the identifiers and tokens (comp words) for the file
            stmnt = sql_driver.createStatement()
            results = stmnt.executeQuery(
                (
                    f"{query_base} '{parsed_file.file_name}"
                    f"{parsed_file.extension}' {query_order}"
                )
            )

            comp_words = []
            identifier_row = None

            # for each result row
            while results.next():
                identifier_name = str(results.getString("identifier_name"))

                # check identifier
                if (
                    identifier_row is not None
                    and identifier_name == current_identifier_name
                    # FIXME current_identifier_name is not initialized
                ):
                    # if identifier is the same, keep collecting comp words
                    comp_words.append(str(results.getString("component_word")))
                    continue

                # when identifier changes, store comp words against old identifier
                self.add_tokens_to_session(
                    tokenizer_helper, comp_words, identifier_row, file_row
                )
                # new comp words list and identifier
                current_identifier_name = identifier_name

                identifier_row = self.add_identifier_to_session(
                    tokenizer_helper=tokenizer_helper,
                    file_row=file_row,
                    identifier_text=current_identifier_name,
                )
                comp_words = [str(results.getString("component_word"))]

            # the final identifier's tokens need to be added
            if len(comp_words) > 0:
                self.add_tokens_to_session(
                    tokenizer_helper, comp_words, identifier_row, file_row
                )
        # commit changes
        self.session.commit()
