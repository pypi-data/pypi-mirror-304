#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License.

from abc import abstractmethod
from typing import List
from ms_recognizers_text.extractor import ExtractResult


class DateTimeListExtractor:

    @abstractmethod
    def extract(self, extract_result, text, reference) -> List[ExtractResult]:
        raise NotImplementedError
