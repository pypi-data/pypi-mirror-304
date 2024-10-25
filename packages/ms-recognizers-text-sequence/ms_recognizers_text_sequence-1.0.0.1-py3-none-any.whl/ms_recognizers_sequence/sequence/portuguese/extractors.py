#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License.

from ms_recognizers_sequence.sequence.config import *
from ms_recognizers_sequence.sequence.config.base_phone_number_configuration import *
from ms_recognizers_sequence.sequence.sequence_recognizer import *
from ms_recognizers_sequence.resources.portuguese_phone_numbers import PortuguesePhoneNumbers
from ms_recognizers_sequence.sequence.extractors import *
from ms_recognizers_text.culture import Culture


class PortuguesePhoneNumberExtractorConfiguration(BasePhoneNumberExtractorConfiguration):

    @property
    def false_positive_prefix_regex(self) -> str:
        return self._false_positive_prefix_regex

    def __init__(self, culture_info: CultureInfo = None):
        super().__init__(culture_info)
        self._false_positive_prefix_regex = PortuguesePhoneNumbers.FalsePositivePrefixRegex
