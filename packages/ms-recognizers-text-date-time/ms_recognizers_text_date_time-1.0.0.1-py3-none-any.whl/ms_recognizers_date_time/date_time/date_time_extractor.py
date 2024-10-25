#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License.

from abc import abstractmethod
from typing import List
from ms_recognizers_text.extractor import ExtractResult
from ms_recognizers_text.extractor import Extractor


class DateTimeExtractor(Extractor):

    @abstractmethod
    def extract(self, text) -> List[ExtractResult]:
        raise NotImplementedError
