"""
Subnetwork :class:, all stations of a network deployed by one operator
"""
# Standard library modules
import warnings
import logging

# Non-standard modules
from obspy.core.inventory.network import Network

# obsinfo modules
from .station import Stations
from .operator import Operators
from ..helpers import (str_indent, str_list_str, verify_dict_is_empty,
                       OIDate, Identifiers, Comments)

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Subnetwork(object):
    """
    Equivalent to obspy/StationXML Network

    Attributes:
         campaign_ref (str): campaign reference name:
         operator_ref (str): operator reference name
         fdsn_code (str)
         fdsn_name (str)
         operators (:class:`Operators`): network operators
         start_date (str with date format): network start date
         end_date (str with date format): network end date
         description  (str): network description
         fdsn_comments (list of str):
         restricted_status (str): 'open', 'closed', or 'partial'
         source_id (str): network-level data source identifier in URI format
         identifiers (list of str): persistent identifiers as URIs, scheme (prefix) will be extracted
         stations_operators (:class:`.Operators`): default operators for all stations
         stations (list of :class:`.Station`)
         comments (list of str)
         extras (list of str)
    """

    def __init__(self, attributes_dict=None, station_only=False):
        """
        Constructor

        Args:
            attributes_dict (dict or :class:`.ObsMetadata`): dictionary from
                network info file
            station_only (bool): Instructs class Station to create object
                with no instrumentation
        Raises:
            (TypeError): if attributes_dict is empty
        """
        if not attributes_dict:
            msg = 'No network attributes'
            logger.error(msg)
            raise TypeError(msg)

        ref_names = attributes_dict.pop("reference_names", None)
        if ref_names is not None:
            self.campaign_ref = ref_names.get("campaign", None)
            self.operator_ref = ref_names.get("operator", None)
        else:
            self.campaign_ref = None
            self.operator_ref = None
        network = attributes_dict.pop("network", None)

        if network:
            self.fdsn_code = network.get("code", None)
            self.fdsn_name = network.get("name", None)
            self.start_date = OIDate(network.get("start_date", None))
            self.end_date = OIDate(network.get("end_date", None))
            self.description = network.get("description", None)
            self.operators = Operators(network.get("operators", None))
            fdsn_comments = Comments(network.get("comments", None))
            self.restricted_status = network.get("restricted_status", None)
            self.source_id = network.get("source_id", None)
            self.identifiers = Identifiers(network.get("identifiers", None))

        self.stations_operators = Operators(attributes_dict.pop("operators"))
        self.stations = Stations(attributes_dict.pop("stations", None),
                                 station_only, self.stations_operators)

        self.comments = Comments(attributes_dict.pop("comments", None))
        self.comments += fdsn_comments
        self.extras = [str(k) + ": " + str(v)
                       for k, v in (attributes_dict.pop('extras', {})).items()]
        self.add_extras_to_comments()
        verify_dict_is_empty(attributes_dict)


    def __str__(self, indent=0, n_subclasses=0):
        if n_subclasses < 0:
            return f'{type(self)}'
        kwargs = {'indent': 4, 'n_subclasses': n_subclasses-1}
        s = f'{self.__class__.__name__}:\n'
        if self.operator_ref is not None:
            s += f'    operator_ref: {self.operator_ref}\n'
        if self.campaign_ref is not None:
            s += f'    campaign_ref: {self.campaign_ref}\n'
        s += f'    fdsn_code: {self.fdsn_code}\n'
        s += f'    fdsn_name: {self.fdsn_name}\n'
        s += f'    operators: {self.operators.__str__(**kwargs)}\n'
        s += f'    start_date: {self.start_date}\n'
        s += f'    end_date: {self.end_date}\n'
        s += f'    description: {self.description}\n'
        s += f'    restricted_status: {self.restricted_status}\n'
        s += f'    stations_operators: {self.stations_operators.__str__(**kwargs)}\n'
        s += f'    stations: {self.stations.__str__(**kwargs)}'
        if len(self.comments) > 0:
            s += f'\n    comments: {str_list_str(self.comments, **kwargs)}'
        if len(self.extras) > 0:
            s += f'\n    extras: {str_list_str(self.extras, **kwargs)}'
        return str_indent(s, indent)

    def to_obspy(self):
        """
         Convert network object to obspy object

         Returns:
            (:class:~obspy.core.inventory.network.Network): corresponding
                obspy Network
        """
        self.obspy_network = Network(
            code=self.fdsn_code,
            stations=self.stations.to_obspy(),
            selected_number_of_stations=len(self.stations),
            description=self.fdsn_name + " - " + self.description,
            comments=self.comments.to_obspy(),
            start_date=self.start_date.to_obspy(),
            end_date=self.end_date.to_obspy(),
            restricted_status=self.restricted_status,
            identifiers=self.identifiers.to_obspy(),
            operators=self.operators.to_obspy(),
            source_id=self.source_id,
            total_number_of_stations=None,
            alternate_code=None,
            historical_code=None,
            data_availability=None)
        return self.obspy_network

    def add_extras_to_comments(self):
        """
        Convert info file extras to XML comments
        """
        if self.extras:
            self.comments += Comments.from_extras(self.extras)
            # self.comments.append('EXTRA ATTRIBUTES (for documentation only):')
            # if isinstance(self.extras, list):
            #     self.comments.extend(self.extras)
            # else:
            #     self.comments.append(self.extras)
# 