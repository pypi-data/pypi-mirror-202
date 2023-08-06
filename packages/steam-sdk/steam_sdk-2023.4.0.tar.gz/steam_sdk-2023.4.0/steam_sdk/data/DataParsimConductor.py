from typing import (List, Dict, Union, Literal)
from pydantic import BaseModel

############################
# General parameters
class GeneralParameters(BaseModel):  # TODO do we need this?
    magnet_name: str = None
    circuit_name: str = None
    state: str = None  # measured, deduced from short-samples, deduced from design

############################
# Magnet
class Magnet(BaseModel):
    coils: List[str] = []
    measured_inductance_versus_current: List[List[float]] = []

############################
# Coils
class Coil(BaseModel):
    ID: str = None
    cable_ID: str = None
    coil_length: float = None
    coil_RRR: float = None
    T_ref_RRR_low: float = None
    T_ref_RRR_high: float = None
    coil_resistance_room_T: float = None
    T_ref_coil_resistance: float = None
    conductors: List[str] = []  # TODO: make sure that names correspond to conductor instances - maybe call it sample?
    weight_conductors: List[float] = []

############################
# Conductors
class IcMeasurement(BaseModel):
    """
        Level 1: Class for parameters of a critical current measurement to adjust Jc fit parameters
    """
    Ic: float = None
    T_ref_Ic: float = None
    B_ref_Ic: float = None
    Cu_noCu_sample: float = None


class Round(BaseModel):
    """
        Level 2: Class for strand parameters
    """
    type: Literal['Round']
    diameter: float = None

class Rectangular(BaseModel):
    """
        Level 2: Class for strand parameters
    """
    type: Literal['Rectangular']
    bare_width: float = None
    bare_height: float = None


class ConductorSample(BaseModel):
    # TODO think of using other conductor class
    ID: str = None
    number_of_strands: int = None
    width: float = None
    height: float = None
    Cu_noCu: float = None
    RRR: float = None
    strand_twist_pitch: float = None
    filament_twist_pitch: float = None
    Ic_measurements: List[IcMeasurement] = []
    Tc0: float = None
    Bc20: float = None
    f_rho_eff: float = None
    Ra: float = None
    Rc: float = None
    strand_geometry: Union[Round, Rectangular] = None


class DataParsimConductor(BaseModel):
    '''
        **Class for the STEAM conductor**

        This class contains the data structure of a Conductor parsim  analyzed with STEAM_SDK.

        :return: DataParsimConductor object
    '''

    GeneralParameters: GeneralParameters = GeneralParameters()
    Magnet: Magnet = Magnet()
    Coils: Dict[str, Coil] = {}
    ConductorSamples: Dict[str, ConductorSample] = {}
