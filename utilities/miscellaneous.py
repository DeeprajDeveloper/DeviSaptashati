import re
from utilities import (custom_error as error)


def match_regex_pattern(data_input, pattern):
    data_match = re.findall(pattern, data_input)
    if len(data_match) > 0:
        if ' ' not in data_match:
            return True
        else:
            raise error.RegexMismatch(f"Data input doesn't match the provided data pattern. Please verify the data inputs and try again.")
    else:
        raise error.RegexMismatch(f"Data input doesn't match the provided data pattern. Please verify the data inputs and try again.")


def check_verse_id_in_range(verse_id, min_value, max_value):
    if verse_id is None:
        raise error.NoContent('Verse ID is a None/NULL value. Please check the data input and retry the search.')
    else:
        if min_value <= verse_id <= max_value:
            return True
        else:
            raise error.VerseIdOutOfRange(f"Verse ID does not fall within the data search range. Value must be contained between {min_value} and {max_value}")
