"""
Stages and Stage classes
"""
# Standard library modules
import warnings
import logging

from ..obsMetadata import ObsMetadata
from .stage import Stage
from ..helpers import ObsinfoClassList

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Stages(ObsinfoClassList):
    """
    Ordered list of :class:`Stage`.
    
    Has a custom constructor using a list of attribute_dicts, and custom
    input_units(), output_units and to_obspy() methods

    Attributes:
        stages (list of objects of :class:`Stage`)
    """
    def __init__(self, attribute_list=None, modifs={},
                 correction=None):  # , ext_config_name=None):
        """
        Constructor

        Args:
            attribute_list (list of dicts): information file
                dictionaries for each stage
            modifs (dict or :class:`.ObsMetadata`):
                modifications to pass down to Stage
            correction (float): used only for datalogger: the delay
                correction for the entire instrument
            # ext_config_name (str): external configuration name applied to
            #     every stage.
        """
        if attribute_list is None:
            msg = 'No stages in information file'
            warnings.warn(msg)
            logger.warning(msg)
            super().__init__([])
            # self.stages = None
        else:
            stages = []
            for s, i in zip(attribute_list, range(0, len(attribute_list))):
                # Assign correction value
                if correction is None:
                    correction = None
                elif i == len(attribute_list)-1:
                    correction = correction
                else:
                    correction = 0
                stages.append(
                    Stage(ObsMetadata(s), modifs, correction, i+1)) # , ext_config_name))
                if i > 0:
                    # Check that input units match prior output units
                    s = stages
                    if not s[i].input_units == s[i-1].output_units:
                        raise ValueError(f'stage {i:d} input units do not '
                                         f'match stage {i-1:d} output units '
                                         '("{}"~="{}")'.format(
                                            s[i].input_units,
                                            s[i-1].output_units))
            super().__init__(stages)


    @property
    def input_units(self):
        return self[0].input_units
        # return self.stages[0].input_units

    @property
    def output_units(self):
        return self[-1].output_units
        # return self.stages[-1].output_units
