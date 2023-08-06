import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

from albert.data.reports import ReportRET28 as unpackReport
from albert.internal.utils import validate_dataframe_has_columns
from albert.pipeline import AlbertConfigurableBaseEstimator


#class HDBSCAN
