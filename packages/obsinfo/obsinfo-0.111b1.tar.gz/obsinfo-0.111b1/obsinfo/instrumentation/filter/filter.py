"""
Filter class and subclasses
"""
# Standard library modules
import warnings
import logging

from .poles_zeros import PolesZeros
from .analog import Analog
from .digital import Digital
from .AD_conversion import ADConversion
from .FIR import FIR
from .response_list import ResponseList
from .coefficients import Coefficients
from .polynomial import Polynomial
from ...obsMetadata import ObsMetadata

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Filter(object):
    """
    Filter is a gateway to the other filter classes
    """
    @staticmethod
    def construct(attributes_dict, stage_id="-1",
                  sensitivity_gain_frequency=1.):
        """
        Constructs an appropriate Filter subclass from an attributes_dict

        Args:
            attributes_dict (dict or list of dicts): information file
                dict for stages
            stage_id (int): id of corresponding stage. Used for reporting only
            sensitivity_gain_frequency (float): frequency at which gain was
                specified.
                Used for PoleZeros Normalization factor/frequency
        Returns:
            (:class:`.Filter`): object of the adequate filter subclass
        Raises:
            (TypeError): if filter type is not valid
        """
        if attributes_dict is None:
            msg = "No attributes in filter"
            logger.error(msg)
            raise TypeError(msg)
        if not isinstance(attributes_dict, ObsMetadata):
            attributes_dict = ObsMetadata(attributes_dict)

        if "type" not in attributes_dict:
            msg = f'No "type" specified for filter in stage #{stage_id}'
            logger.error(msg)
            raise TypeError(msg)
        else:
            filter_type = attributes_dict.get('type', None)
            if filter_type == 'PolesZeros':
                attributes_dict['sensitivity_gain_frequency'] = sensitivity_gain_frequency
                obj = PolesZeros(attributes_dict, stage_id)
            elif filter_type == 'FIR':
                obj = FIR(attributes_dict, stage_id)
            elif filter_type == 'Coefficients':
                obj = Coefficients(attributes_dict, stage_id)
            elif filter_type == 'ResponseList':
                obj = ResponseList(attributes_dict, stage_id)
            elif filter_type == 'ADCONVERSION':
                obj = ADConversion(attributes_dict, stage_id)
            elif filter_type == 'ANALOG':
                attributes_dict['sensitivity_gain_frequency'] = sensitivity_gain_frequency
                obj = Analog(attributes_dict, stage_id)
            elif filter_type == 'DIGITAL':
                obj = Digital(attributes_dict, stage_id)
            elif filter_type == 'Polynomial':
                obj = Polynomial(attributes_dict, stage_id)
            else:
                msg = (f'Unknown Filter type: "{filter_type}" in '
                       'stage #{stage_id}')
                logger.error(msg)
                raise TypeError(msg)
        return obj
