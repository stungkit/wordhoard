#!/usr/bin/env python3

"""
This Python script is designed to query internal repositories for the
homophones associated with the given word.
"""
__author__ = 'John Bumgarner'
__date__ = 'June 12, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

##################################################################################
# “AS-IS” Clause
#
# Except as represented in this agreement, all work produced by Developer is
# provided “AS IS”. Other than as provided in this agreement, Developer makes no
# other warranties, express or implied, and hereby disclaims all implied warranties,
# including any warranty of merchantability and warranty of fitness for a particular
# purpose.
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import sys
import pickle
import logging
import traceback
from wordhoard.utilities import caching, wordhoard_logger, word_verification

logger = logging.getLogger(__name__)
wordhoard_logger.enable_logging(logger)


# Opening the pickle file that contains a nested list of common
# English language homophones.
try:
    with open('files/common_english_homophones.pkl', 'rb') as eng_homophones:
        known_homophones_list = pickle.load(eng_homophones)
        eng_homophones.close()
except FileNotFoundError as e:
    logger.error('The common_english_homophones.pkl file was not found. Aborting operation.')
    logger.error(''.join(traceback.format_tb(e.__traceback__)))
    sys.exit(1)
except OSError as e:
    logger.error(f"An OS error occurred when trying to open the file common_english_homophones.pkl")
    logger.error(''.join(traceback.format_tb(e.__traceback__)))
    sys.exit(1)


# Opening the pickle file that contains a nested list of English
# language words that have no known homophones.
try:
    with open('files/no_homophones_english.pkl', 'rb') as no_eng_homophones:
        no_homophones_list = pickle.load(no_eng_homophones)
        no_eng_homophones.close()
except FileNotFoundError as e:
    logger.error('The no_homophones_english.pkl file was not found. Aborting operation.')
    logger.error(''.join(traceback.format_tb(e.__traceback__)))
    sys.exit(1)
except OSError as e:
    logger.error(f"An OS error occurred when trying to open the file no_homophones_english.pkl")
    logger.error(''.join(traceback.format_tb(e.__traceback__)))
    sys.exit(1)


def common_english_homophones(search_string):
    """
    This function iterates through a list of known
    English language homophones.

    :param search_string: string variable to search for
    :return: list of homophones
    :rtype: list
    """
    global known_homophones_list
    rtn_list = []
    for homophones in known_homophones_list:
        match = bool([word for word in homophones if word == search_string])
        if match:
            for word in homophones:
                if word != search_string:
                    rtn_list.append(f'{search_string} is a homophone of {word}')
    if len(rtn_list) > 0:
        return list(set(rtn_list))


def english_words_without_homophones(search_string):
    """
    This function iterates through a list of English
    language words with no known homophones.

    :param search_string: string variable to search for
    :return: string
    :rtype: string
    """
    global no_homophones_list
    match = bool(search_string in no_homophones_list)
    if match:
        return f'no homophones for {search_string}'


def query_homophones(search_string):
    """
    This function queries multiple lists to
    find an English language homophones for
    the a specific word.

    :param search_string: string variable to search for
    :return: list of homophones or string
    :rtype: list or string
    """
    valid_word = word_verification.validate_word_syntax(search_string)
    if valid_word:
        known_english_homophones = common_english_homophones(search_string)
        if known_english_homophones:
            return known_english_homophones
        elif not known_english_homophones:
            return english_words_without_homophones(search_string)
    else:
        logger.error(f'The word {search_string} was not in a valid format.')
        logger.error(f'Please verify that the word {search_string} is spelled correctly.')


results = query_homophones('horse')
print(results)