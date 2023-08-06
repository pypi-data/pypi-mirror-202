"""
stores dates and converts to UTCDateTime
"""
# Standard library modules
import warnings
import logging
import re

# Non-standard modules
from obspy.core import UTCDateTime

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class OIDate(object):
    """
    Store dates before converting to UTCDateTime

    Attributes:
        date
    """
    def __init__(self, datestr):
        """
        Create object and assign attributes from attributes_dict.

        Args:
            attributes_dict (dict or :class:`ObsMetadata`): dict with
                relevangt keys
        """
        self.date = self.validated_date(datestr)

    def __str__(self):
        if self.date is None:
            return('None')
        return(self.date)

    def __repr__(self):
        return f"OIDate('{self.date}')"

    def __eq__(self, other):
        if not isinstance(other, OIDate):
            return False
        return self.date == other.date

    def to_obspy(self):
        """
        Return UTCDateTime object:
        """
        if self.date is None:
            return None
        return UTCDateTime(self.date)

    @staticmethod
    def validated_date(str_date):
        """
        Reformats an individual date string

        Uses regular expressions to match known dates, either in UTC date
        format, in UTC date and time format or in regular dd-mm-yyyy format.
        If only two digits of year specified, assumes 21st century.
        The separator can be either "/" or "-"

        Args:
            date (str): a date in a given format
        Returns:
            (str): a reformatted date as string or None if no value
        Raises:
            (ValueError) if date is unrecognizable
        """
        if str_date is None or str_date == int(0):
            # 0 is sometimes the default, the epoch date, 1/1/1970
            return None

        regexp_date_UTC = re.compile(r"^[0-9]{4}[-\/][0-1]{0,1}[0-9][-\/][0-3]{0,1}[0-9]")
        regexp_date_and_time_UTC = re.compile(r"^[0-9]{4}[-\/][0-1]{0,1}[0-9][-\/][0-3]{0,1}[0-9]T[0-2][0-9]:[0-6][0-9]:{0,1}[0-6]{0,1}[0-9]{0,1}Z{0,1}")
        if (re.match(regexp_date_UTC, str_date) or re.match(regexp_date_and_time_UTC, str_date)):
            return str_date
        else:  # Assume it's a regular date
            warnings.warn(f'Date {str_date} is not UTC format, assuming '
                          'regular dd/mm/yyyy format')
            # regexp_date_normal = re.compile("[\-\/]")
            regexp_date_normal = re.compile(r"[-\/]")
            date_elements = re.split(regexp_date_normal, str_date)
            if len(date_elements) != 3:
                raise ValueError("Unrecognizable date, must either be UTC or "
                                 "dd/mm/yyyy or dd/mm/yy. Dashes can be used "
                                 "as separators")
            if len(date_elements[2]) == 2:
                date_elements[2] = "20" + date_elements[2]
                warnings.warn(f"Date {str_date}'s year is two digits, "
                              "prepending '20'")

            return f'{date_elements[2]}-{date_elements[1]}-{date_elements[0]}'

    @staticmethod
    def validated_dates(dates):
        """
        Convert list of dates to a standard format

        Args:
            dates (list): dates as strings
        Returns:
            (list): formatted dates as strings
        """
        if dates is None or not isinstance(dates, list):
            return []
        else:
            return [OIDate.validated_date(dt) for dt in dates]
