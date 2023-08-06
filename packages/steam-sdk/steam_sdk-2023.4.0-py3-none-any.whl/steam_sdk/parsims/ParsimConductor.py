import csv
import math
import warnings
import time

import numpy as np
import pandas as pd
import os
from typing import List, Dict

from steam_sdk.data.DataParsimConductor import DataParsimConductor, Coil, Round, Rectangular, IcMeasurement
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.sgetattr import rsetattr, rgetattr
from steam_sdk.data.DataParsimConductor import ConductorSample
# TODO why dont we just use Conductor from DataConductor and read all the data into that class and then write the csv from that class?



class ParsimConductor:
    """

    """

    def __init__(self, model_data_conductors, verbose: bool = True):
        """
        If verbose is read to True, additional information will be displayed
        """
        # Unpack arguments
        self.model_data_conductors = model_data_conductors
        self.verbose: bool = verbose

        # DataParsimConductor object that will hold all the information from the input csv file
        self.data_parsim_conductor = DataParsimConductor()

    def read_from_input(self, path_input_file: str, magnet_name: str, strand_critical_current_measurements: Dict[str, Dict]):
        '''
        Read a .csv file and assign its content to a instance of DataParsimConductor().

        Parameters:
            path_input_file: Path to the .csv file to read
            magnet_name: name of the magnet that should be changed
            strand_critical_current_measurements: dict of all the critical current measurements specified by the user
        '''

        # read table into pandas dataframe
        if path_input_file.endswith('.csv'):
            df_conductors = pd.read_csv(path_input_file)
        elif path_input_file.endswith('.xlsx'):
            df_conductors = pd.read_excel(path_input_file)
        else:
            raise Exception(f'The extension of the file {path_input_file} is not supported. Use either csv or xlsx.')
        df_conductors = df_conductors.dropna(axis=1, how='all')

        # set magnet name to local model
        rsetattr(self.data_parsim_conductor, 'GeneralParameters.magnet_name', magnet_name)

        # get column name of coil and magnet
        parsed_columns = []  # list containing the column names that were parsed
        column_name_magnets, column_name_coils = self.__get_and_check_main_column_names(df_conductors, parsed_columns)

        # delete all rows of dataframe that don't belong to the magnet
        mask = df_conductors[column_name_magnets] != magnet_name  # create a boolean mask for the rows that do not have the value in the column
        df_conductors = df_conductors.drop(df_conductors[mask].index)  # drop the rows that do not have the value in the column

        # Assign the content to a dataclass structure - loop over all the coils of the magnet in the database
        for _, row in df_conductors.iterrows():
            self.__read_magnet(row, column_name_coils, parsed_columns)
            self.__read_coils(row, column_name_coils, parsed_columns)
            self.__read_conductors(row, column_name_coils, parsed_columns, strand_critical_current_measurements)

        # show the user all the columns that where ignored by the code
        ignored_column_names = list(set(df_conductors.columns) - set(parsed_columns))
        if self.verbose: print(f'Names of ignored columns: {ignored_column_names}')

    def write_conductor_parameter_file(self, path_output_file: str, simulation_name: str, simulation_number: int,
                                       dict_coilname_to_conductorindex: Dict[str, int]):
        """
        Write the Parsim Conductor information to a CSV file, that can be used to run a ParsimSweep Step.

        Parameters:
            path_output_file (str): path to the output file
        """

        # Make target folder if it is missing
        make_folder_if_not_existing(os.path.dirname(path_output_file))

        # save all conductor parameters in a dict
        dict_sweeper = dict()
        dict_sweeper['simulation_name'] = simulation_name
        dict_sweeper['simulation_number'] = int(simulation_number)
        # self.__write_parsweep_general_parameters(dict_sweeper) # no function needed, just one line of code
        self.__write_parsweep_magnet(dict_sweeper)
        self.__write_parsweep_coils(dict_sweeper)
        self.__write_parsweep_conductors(dict_sweeper, dict_coilname_to_conductorindex)

        # open file in writing mode and write the dict of the parameters as a row in the sweeper csv file
        with open(path_output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=dict_sweeper.keys())
            writer.writeheader()
            writer.writerow(dict_sweeper)

    ################ HELPERS

    def __get_and_check_main_column_names(self, df_conductors, parsed_columns):
        '''
            TODO refactoring and docstrings
        '''
        # allowed names for the magnet
        csv_column_names_for_magnet_name = ['Magnet', 'Magnet Name', 'magnet', 'magnet name']
        csv_column_names_for_coil_name = ['Coil', 'Coil Name', 'coil', 'coil name']

        # find out what name is being used for the magnet and coil column
        column_name_magnets, column_name_coils = None, None
        for col_name_magnet in csv_column_names_for_magnet_name:
            if col_name_magnet in df_conductors.keys():
                column_name_magnets = col_name_magnet
        for col_name_coil in csv_column_names_for_coil_name:
            if col_name_coil in df_conductors.keys():
                column_name_coils = col_name_coil
        # TODO do i check later if coilnames are valid?

        # check if there is a column for magnet and coil
        if not column_name_magnets:
            raise Exception(f'No column for the magnet name could be found in the input table. Make sure this column is present.\nAllowed values :{csv_column_names_for_magnet_name}')
        if not column_name_coils:
            raise Exception(f'No column for the coil names could be found in the input table. Make sure this columns are present.\nAllowed values:{csv_column_names_for_coil_name}')

        # check if magnet name is present in the xlsx file
        if not any(df_conductors[column_name_magnets] == self.data_parsim_conductor.GeneralParameters.magnet_name):
            raise Exception(f'The magnet "{self.data_parsim_conductor.GeneralParameters.magnet_name}" is not present in the conductor database. ')

        # and mark columns as parsed
        parsed_columns.append(column_name_magnets)
        parsed_columns.append(column_name_coils)

        return column_name_magnets, column_name_coils


    def __read_general_parameters(self, magnet_name):
        rsetattr(self.data_parsim_conductor, 'GeneralParameters.magnet_name', magnet_name)


    def __read_magnet(self, row, column_name_coils, parsed_columns):
        # add coil name to Coils list
        self.data_parsim_conductor.Magnet.coils.append(row[column_name_coils])


    def __read_coils(self, row, column_name_coils, parsed_columns):
        '''
            Parses a row of the conductor input csv and creates a Coil instance for the current magnet.

            Args:
                row (pandas.Series): a row of the coils input file
                parsed_columns (list): a list of parsed column names

            Raises:
                Exception: if the coil name is not valid or has been used before
        '''

        # create Coil instance
        coil_name = row[column_name_coils]
        new_Coil = Coil()

        # check if coil name is valid
        if coil_name not in self.data_parsim_conductor.Magnet.coils:
            raise Exception(
                'Unexpected error in steam_sdk.parsims.ParsimConductor.__read_coils(). Coil name previously not found.')
        if coil_name in self.data_parsim_conductor.Coils.keys():
            raise Exception(
                f'Coil names of the magnet {self.data_parsim_conductor.GeneralParameters.magnet_name} in column {column_name_coils} have to be unique. Name {coil_name} has been used before.')

        # change parameters of conductors instance
        dict_params = {
            'Estimated coil RRR': 'coil_RRR',
            # 'Coil ID': 'ID', 'ID': 'ID',
            # 'Cable ID': 'cable_ID', 'cable_ID': 'cable_ID',
            # 'Coil length': 'coil_length', 'Coil length [m]': 'coil_length', 'Coil length [mm]': 'coil_length',
            # 'coil_length': 'coil_length', 'coil length / half/turns [m]': 'coil_length',
            # 'coil length / half/turns [mm]': 'coil_length',
            # 'tot coil length [m]': 'coil_length', 'tot coil length [mm]': 'coil_length',
            # 'tot coil length': 'coil_length',  # TODO check if this is correct
            # 'Coil RRR': 'coil_RRR', 'coil_RRR': 'coil_RRR',
            # 'Tref RRR low': 'T_ref_RRR_low', 'T_ref_RRR_low': 'T_ref_RRR_low',
            # 'Tref RRR high': 'T_ref_RRR_high', 'T_ref_RRR_high': 'T_ref_RRR_high',
            # 'Coil resistance room T': 'coil_resistance_room_T', 'coil_resistance_room_T': 'coil_resistance_room_T',
            # 'RT coil resistance [Ohm]': 'coil_resistance_room_T', 'RT coil resistance': 'coil_resistance_room_T',
            # 'Tref coil resistance': 'T_ref_coil_resistance', 'T_ref_coil_resistance': 'T_ref_coil_resistance',
        }
        for csv_col_name, coil_param_name in dict_params.items():
            if csv_col_name in row:
                # check dimension of input column to convert number into SI unit
                dim = csv_col_name[csv_col_name.find('[') + 1:csv_col_name.find(']')] if '[' in csv_col_name else ''
                # change parameter is not null and convert number into SI unit
                if not pd.isna(row[csv_col_name]):
                    # if the RRR value is a list, use the mean value of the list
                    if coil_param_name is 'coil_RRR' and type(row[csv_col_name]) == str: # TODO function: get_mean_from_stringlist() and use it everywhere - maybe also with weight factor
                        if '[' not in row[csv_col_name] or ']' not in row[csv_col_name]:
                            raise Exception(f'Invalid input format in column "{csv_col_name}". Please specify RRR eighter with just a number (e.g. "190") or with a list (e.g. "[190, 200]"). The code will then use the mean value of the list.')
                        val_list = [float(x) for x in row[csv_col_name].strip("[]").split(",")]
                        mean_val = sum(val_list) / len(val_list)
                        rsetattr(new_Coil, coil_param_name, make_value_SI(mean_val, dim))
                    else:
                        rsetattr(new_Coil, coil_param_name, make_value_SI(row[csv_col_name], dim))
                # mark column as parsed
                if csv_col_name not in parsed_columns: parsed_columns.append(csv_col_name)

        # set Conductor of the Coil and set weightfactor to 1.0
        new_Coil.conductors.append(f'conductor_{coil_name}')
        new_Coil.weight_conductors = [1.0]  # TODO: by default avg - when weight factor specified: use that

        # append new coil instance to Coil Dict of ParsimConductor
        self.data_parsim_conductor.Coils.update({coil_name: new_Coil})

    def __read_conductors(self, row, column_name_coils, parsed_columns, strand_critical_current_measurements):
        '''
        Function to read Conductors of ParsimConductors

        :param row: Series of parameters (read from csv file)
        :param parsed_columns: list of parsed table columns names
        '''

        # create Conductor instance
        coil_name = row[column_name_coils]
        cond_name = f'conductor_{coil_name}'
        new_Conductor = ConductorSample()

        # read the critical current measurements into the local conductor dataclass
        for meas in strand_critical_current_measurements:
            if coil_name in meas.coil_names:
                # create new IcMeasurement instance, add all values and append it to the measurement list of the conductor
                new_Ic_meas = IcMeasurement()
                # add temperature and magnetic flux of the measurements (directly given in step definition)
                rsetattr(new_Ic_meas, 'B_ref_Ic', meas.reference_mag_field)
                rsetattr(new_Ic_meas, 'T_ref_Ic', meas.reference_temperature)
                # read critical current form csv file
                if meas.column_name_I_critical in row and not pd.isna(row[meas.column_name_I_critical]):
                    dim = meas.column_name_I_critical[meas.column_name_I_critical.find('[') + 1:meas.column_name_I_critical.find(']')] if '[' in meas.column_name_I_critical else ''
                    rsetattr(new_Ic_meas, 'Ic', make_value_SI(row[meas.column_name_I_critical], dim))
                else:
                    raise Exception(f'Provided coulumn name for Ic measurement "{meas.column_name_I_critical}" was not found in the conductor database or is empty.')
                # read CuNoCu ratio of the short sample measurement
                if meas.column_name_CuNoCu_short_sample in row and not pd.isna(row[meas.column_name_CuNoCu_short_sample]):
                    dim = meas.column_name_CuNoCu_short_sample[meas.column_name_CuNoCu_short_sample.find('[') + 1:meas.column_name_CuNoCu_short_sample.find(']')] if '[' in meas.column_name_CuNoCu_short_sample else ''
                    rsetattr(new_Ic_meas, 'Cu_noCu_sample', make_value_SI(row[meas.column_name_CuNoCu_short_sample], dim))
                else:
                    raise Exception(f'Provided coulumn name for Ic measurement "{meas.column_name_CuNoCu_short_sample}" was not found in the conductor database or is empty.')
                new_Conductor.Ic_measurements.append(new_Ic_meas)


            # check if Conductor name is is valid (new conductor name corresponds to a conductor name already specified in a Coil)
            if cond_name not in sum([coil.conductors for coil in self.data_parsim_conductor.Coils.values()], []):
                raise Exception('Unexpected error in steam_sdk.parsims.ParsimConductor.__read_conductors(). Conductor name previously not found.')

            # dict for parsing csv entries into local Conductor class
            dict_params = {
                'Ds [m]': 'strand_geometry.diameter', 'Ds [mm]': 'strand_geometry.diameter', 'strand_diameter': 'strand_geometry.diameter',
                'Tc0 [K]': 'Tc0', 'Tc0': 'Tc0',
                'Bc20 [T]': 'Bc20', 'Bc20': 'Bc20',
                'bare strand width': 'strand_geometry.bare_width', 'strand width': 'strand_geometry.bare_width',
                'bare strand height': 'strand_geometry.bare_height', 'strand height': 'strand_geometry.bare_height',
                # 'Shape': 'shape', 'shape': 'shape',
                # 'Number of strands': 'number_of_strands', 'number_of_strands': 'number_of_strands',
                'width [m]': 'width', 'width [mm]': 'width', 'width': 'width',
                # 'Height [m]': 'height', 'Height [mm]': 'height', 'height': 'height',
                # 'Cu noCu': 'Cu_noCu', 'Cu_noCu': 'Cu_noCu', 'Ave Cu/noCu': 'Cu_noCu',
                # 'RRR [-]': 'RRR',
                'Strand twist pitch': 'strand_twist_pitch', 'strand_twist_pitch': 'strand_twist_pitch',
                'Strand twist-pitch [m]': 'strand_twist_pitch', 'Strand twist-pitch [mm]': 'strand_twist_pitch',
                'Filament twist pitch': 'filament_twist_pitch', 'filament_twist_pitch': 'filament_twist_pitch',
                'Fil twist-pitch [mm]': 'filament_twist_pitch', 'Fil twist-pitch [m]': 'filament_twist_pitch',
                # 'F rho eff': 'f_rho_eff', 'f_rho_eff': 'f_rho_eff',
                # 'Ra [Ohm]': 'Ra',
                # 'Rc [Ohm]': 'Rc'
            }


            # change parameters of conductors instance
            for csv_col_name, conductor_name in dict_params.items():
                if csv_col_name in row:
                    # check dimension of input column to convert number into SI unit
                    dim = csv_col_name[csv_col_name.find('[') + 1:csv_col_name.find(']')] if '[' in csv_col_name else ''
                    # check if value is set in csv file
                    if not pd.isna(row[csv_col_name]):
                        # set geometry object (Round, Rectangular) of conductor
                        if 'strand_geometry' in conductor_name: self.__set_conductor_geometry(new_Conductor, conductor_name)
                        # change parameter and convert number into SI unit
                        rsetattr(new_Conductor, conductor_name, make_value_SI(row[csv_col_name], dim))
                    # mark column as parsed
                    if csv_col_name not in parsed_columns: parsed_columns.append(csv_col_name)

            # read coil RRR and insert it into the conductor
            new_Conductor.RRR = self.data_parsim_conductor.Coils[row[column_name_coils]].coil_RRR

            # append new conductor instance to Conductors dictionary of ParsimConductor
            self.data_parsim_conductor.ConductorSamples.update({cond_name: new_Conductor})

    def __set_conductor_geometry(self, new_Conductor, conductor_name: str):
        # NOTE: the user can either specify the strand diameter or the strand bare width/height
        #   - based on what he specifies either a Round or a Rectangular object is created
        #   - when he tries to provide both an error will be raised

        geometry_property = conductor_name.split('strand_geometry.')[1]

        # if geometry object is not set, add the object that corresponds to entries in the csv that the user wants to change
        if not new_Conductor.strand_geometry:
            if geometry_property == 'diameter':
                new_Conductor.strand_geometry = Round(type='Round')
            elif geometry_property in ['bare_width', 'bare_height']:
                new_Conductor.strand_geometry = Rectangular(type='Rectangular')
            else:
                raise Exception(f'Tried to set an unknown geometry property. "{conductor_name}" not defined in DataParsimConductor.')

        # if a geometry object is set, check if the parameter that the user wants to change is in line with the shape of the conductor
        if new_Conductor.strand_geometry:
            if geometry_property == 'diameter':
                if not isinstance(new_Conductor.strand_geometry, Round):
                    raise Exception('Tried to set diameter after previously setting strand width/height. Only define either diameter or width/height depending on the shape of the conductor.')
            elif geometry_property in ['bare_width', 'bare_height']:
                if not isinstance(new_Conductor.strand_geometry, Rectangular):
                    raise Exception('Tried to set strand width/height after previously setting strand diameter. Only define either diameter or width/height depending on the shape of the conductor.')
            else:
                raise Exception(f'Tried to set an unknown geometry property. "{conductor_name}" not defined in DataParsimConductor.')



    def __write_parsweep_magnet(self, dict_sweeper):
        # TODO conversion of the conductor groups
        # TODO Jc fit parameters from Ic measurements
        # TODO calculate average f_Cu
        # TODO calculate average RRR
        # TODO calculate coil length based on RT resistance
        pass

    def __write_parsweep_coils(self, dict_sweeper):
        pass

    def __write_parsweep_conductors(self, dict_sweeper, dict_coilname_to_conductorindex):
        """
        Writes the Conductor parameter for a sweeper csv file to a dict.

        Parameters:
        - dict_sweeper (dict): input dict where the sweeper entries will be stored  int the format {columnName: value}
        - dict_coilname_to_conductorindex (dict): input dict that specifies what column corresponds to what conductor index in the model {coilName: conductorIndex}

        """
        # parameter dict for creating the column names of sweeper csv file
        dict_param = {
            # format {parameter_name_of_conductor_object: parameter_name_of_DataModelMagnet_object}
            'strand_geometry.diameter': 'strand.diameter',
            'RRR': 'strand.RRR',
            'width': 'cable.bare_cable_width',  # TODO is this correct?
            'filament_twist_pitch': 'strand.fil_twist_pitch',
            'strand_twist_pitch': 'cable.strand_twist_pitch',
        }

        # looping through the conductor list
        for conductor_name, conductor in self.data_parsim_conductor.ConductorSamples.items():
            # get the number of the conductor from his name
            coil_name = conductor_name[len("conductor_"):]
            if coil_name in dict_coilname_to_conductorindex:
                idx = dict_coilname_to_conductorindex[coil_name]
            else:
                raise Exception(f'Conductor named "{coil_name}" could not be found in conductor database.')
            sweeper_cond_name = f'Conductors[{idx}].'

            # parse data from DataParsimConductor to strings for sweeper csv and store them in dict_sweeper
            for cond_object_name, sweeper_name in dict_param.items():
                # skip parameters of strand_geometry if the geometry was never set, meaning no strand geometry value was provided
                if 'strand_geometry' in cond_object_name and not conductor.strand_geometry:
                    continue
                if rgetattr(conductor, cond_object_name):
                    # check if conductor is rutherford before changing strand twist pitch
                    if cond_object_name == 'strand_twist_pitch' and self.model_data_conductors[idx].cable.type != 'Rutherford':
                        raise Exception(f'Tried to change strand twist pitch property of a non Rutherford cable.')
                    # add value to the sweeper dict
                    dict_sweeper[sweeper_cond_name + sweeper_name] = rgetattr(conductor, cond_object_name)

            # insert Jc fit value(s) depending on their fitting function (usual Bottura, CUDI1, CUDI3 for NbTi and Summers, Bordini for Nb3Sn)
            Jc_dict = get_Jc_fit_params(original_conductor=self.model_data_conductors[idx], strand_geometry=conductor.strand_geometry,
                                        Ic_measurements=conductor.Ic_measurements, Tc0=conductor.Tc0, Bc20=conductor.Bc20,
                                        coil_name=coil_name, mag_name=self.data_parsim_conductor.GeneralParameters.magnet_name)
            for name, val in Jc_dict.items():
                if val: dict_sweeper[sweeper_cond_name + 'Jc_fit.' + name] = val


def get_Jc_fit_params(original_conductor, strand_geometry, Tc0, Bc20, Ic_measurements, coil_name, mag_name):
    # TODO: use C-python-wrapper functions(see steam-materials-library) - ask Mariusz how to set it up (when it is implemented)
    if original_conductor.Jc_fit.type == 'Summers':
        # check inputs
        if not original_conductor.strand.type: raise Exception(f'Strand type of conductor in coil {coil_name} is not specified in modelData.')
        if len(Ic_measurements) > 1:
            raise Exception(f'More then one Measurement for Summers fit provided for coil {coil_name}. Please only provide 1 or 0.')
        elif len(Ic_measurements) < 1:
            warnings.warn(f'No Measurement for Summers fit provided for coil {coil_name}. Calculation of new Summers parameters will be skipped.')
            return {}
        else:
            Ic_measurement = Ic_measurements[0]
            if not Ic_measurement.Ic: raise Exception(f'No measured critical current (Ic) for Summers fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not Ic_measurement.B_ref_Ic: raise Exception(f'No reference magnetic field of critical current measurement for Summers fit provided for coil {coil_name}.')
            if not Ic_measurement.T_ref_Ic: raise Exception(f'No reference temperature of critical current measurement for Summers fit provided for coil {coil_name}.')
            if not Ic_measurement.Cu_noCu_sample: raise Exception(f'No Cu-nCu-ratio of critical current measurement for Summers fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
        
        # use parameters of modelData if they are not changed with the conductor database
        if not Tc0: Tc0 = original_conductor.Jc_fit.Tc0_Summers
        if not Bc20: Bc20 = original_conductor.Jc_fit.Bc20_Summers

        # calculate critical current density from critical current by using the area of
        fCu = Ic_measurement.Cu_noCu_sample / (Ic_measurement.Cu_noCu_sample+1)
        A = calc_strand_area(strand_geometry, original_conductor)
        A_noCu = A * (1-fCu)
        Jc_Tref_Bref = Ic_measurement.Ic/A_noCu

        # search for the best C0
        tol = 1e-6  # hardcoded
        if original_conductor.Jc_fit.Jc0_Summers:
            val_range = [original_conductor.Jc_fit.Jc0_Summers / 1000, original_conductor.Jc_fit.Jc0_Summers * 1000]
            print(val_range)
        else: val_range = [1e6, 1e14]
        n_iterations = math.ceil(np.log((val_range[1]-val_range[0])/tol) / np.log(10))  # from formula: width/(10**n_iterations) = tol
        start_time = time.time()
        print(f'number of iterations: {n_iterations}')
        for _ in range(n_iterations):
            try_CO_Summers = np.linspace(val_range[0], val_range[1], 10)
            tryJc_Summers = np.zeros(len(try_CO_Summers))
            # calculate Jc for every selected C0 value
            for j in range(len(try_CO_Summers)):
                tryJc_Summers[j] = Jc_Nb3Sn_Summer_new(Ic_measurement.T_ref_Ic, Ic_measurement.B_ref_Ic, try_CO_Summers[j], Tc0, Bc20)
            # find indices of the list values that are higher than Jc_Tref_Bref
            tempIdx = np.where(np.array(tryJc_Summers) >= Jc_Tref_Bref)[0]
            if len(tempIdx) == 0: raise Exception('No C0 for Jc Summers fit could be found in specified value range.')
            # set new value range for net iteration
            val_range = [try_CO_Summers[tempIdx[0]-1], try_CO_Summers[tempIdx[0]]]
            C0 = try_CO_Summers[tempIdx[0]-1]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for summers: {elapsed_time:.2f} seconds")

        return {
                'Jc0_Summers': C0,
                'Tc0_Summers': Tc0,
                'Bc20_Summers': Bc20,
                }
    elif original_conductor.Jc_fit.type == 'Bordini':
        # TODO use C-function when wrapper is available
        return {
                'C0_Bordini': todo(),
                'alpha_Bordini': todo(),
                'Tc0_Bordini': todo(),
                'Bc20_Bordini': todo(),
                }
    elif original_conductor.Jc_fit.type == 'CUDI1':
        # general equation for CUDI1: Ic = (C1 + C2*B) * (1 - T/Tc0*(1-B/Bc20)^-.59)

        # depending on the number of critical current measurements, use different ways to calculate C1 and C2 parameter
        if len(Ic_measurements) > 2:
            raise Exception(f'More then two measurements for CUDI1 fit provided in coil {coil_name}. Please only provide 2, 1 or 0.')
        elif len(Ic_measurements) == 2:
            # if two measurements are specified, we have 2 equations and 2 unknowns -> system can be solved

            # check inputs and use parameters of modelData if they are not changed with the conductor database
            for Ic_measurement in Ic_measurements:
                if not Ic_measurement.Ic: raise Exception(f'No measured critical current (Ic) for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
                if not Ic_measurement.B_ref_Ic: raise Exception(f'No reference magnetic field of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
                if not Ic_measurement.T_ref_Ic: raise Exception(f'No reference temperature of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
                if not Ic_measurement.Cu_noCu_sample: raise Exception(f'No Cu-nCu-ratio of critical current measurement for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not original_conductor.cable.n_strands: raise Exception('No number of strands specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Tc0_CUDI1: raise Exception('No Tc0 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Bc20_CUDI1: raise Exception('No Bc02 specified in modelData of the conductor that should be changed.')
            if not Tc0: Tc0 = original_conductor.Jc_fit.Tc0_CUDI1
            if not Bc20: Bc20 = original_conductor.Jc_fit.Bc20_CUDI1

            # convert critical current of strand to critical current of conductor by multiplying with number of strands
            Ic_cable1 = Ic_measurements[0].Ic * original_conductor.cable.n_strands
            Ic_cable2 = Ic_measurements[1].Ic * original_conductor.cable.n_strands

            # solve system of linear equations: A*x = b
            A = np.array([[1, Ic_measurements[0].B_ref_Ic], [1, Ic_measurements[1].B_ref_Ic]])
            b_1 = Ic_cable1 / (1 - Ic_measurements[0].T_ref_Ic / Tc0 * (1 - Ic_measurements[0].B_ref_Ic / Bc20) ** -0.59)
            b_2 = Ic_cable2 / (1 - Ic_measurements[1].T_ref_Ic / Tc0 * (1 - Ic_measurements[1].B_ref_Ic / Bc20) ** -0.59)
            b = np.array([b_1, b_2])
            x = np.linalg.solve(A, b)
            if len(x) == 2:
                C1, C2 = x
            else:
                raise Exception(f'No valid solution for CUDI fitting parameters C1 and C2 could be found for coil {coil_name}.')
        elif len(Ic_measurements) == 1:
            # if only one measurement is provided use one equation and the ratio of C1 and C2 according to modelData and warn the user
            warnings.warn(f'Only one Measurement for CUDI fit provided for coil {coil_name}. Ratio of C1 and C2 from modelData is used as a second equation.')

            # check inputs and use parameters of modelData if they are not changed with the conductor database
            if not Ic_measurements[0].Ic: raise Exception(f'No measured critical current (Ic) for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not Ic_measurements[0].B_ref_Ic: raise Exception(f'No reference magnetic field of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
            if not Ic_measurements[0].T_ref_Ic: raise Exception(f'No reference temperature of critical current measurement for CUDI1 fit provided for coil {coil_name}.')
            if not Ic_measurements[0].Cu_noCu_sample: raise Exception(f'No Cu-nCu-ratio of critical current measurement for CUDI1 fit could be found in conductor database for coil {coil_name}. Please check column name in step definition.')
            if not original_conductor.cable.n_strands: raise Exception('No number of strands specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Tc0_CUDI1: raise Exception('No Tc0 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.Bc20_CUDI1: raise Exception('No Bc02 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.C1_CUDI1: raise Exception('No C1_CUDI1 specified in modelData of the conductor that should be changed.')
            if not original_conductor.Jc_fit.C2_CUDI1: raise Exception('No C2_CUDI1 specified in modelData of the conductor that should be changed.')
            if not Tc0: Tc0 = original_conductor.Jc_fit.Tc0_CUDI1
            if not Bc20: Bc20 = original_conductor.Jc_fit.Bc20_CUDI1

            # convert critical current of strand to critical current of conductor by multiplying with number of strands
            Ic_cable1 = Ic_measurements[0].Ic * original_conductor.cable.n_strands

            # try to read C1 over C2 ratio from modelData - if not existing use usual ratio for NbTi superconductors
            if not original_conductor.Jc_fit.C1_CUDI1 or not original_conductor.Jc_fit.C2_CUDI1:
                warnings.warn(f'No C1 or C2 parameter defined in modelData for coil {coil_name}. Using usual ratio for NbTi superconductors.')
                # 92073.5 and -6869.4 are hardcoded values come from magnet "MB inner layer" in csv file "Strand and cable characteristics"
                # atan2 is a tangens calcualtion that also saves the sign of the angle
                angle_C1_C2 = math.atan2(92073.5, -6869.4)  # saving signed angle instead of ratio to have correct signs - tan(angle_C1_C2) = C1/C2
            else:
                angle_C1_C2 = math.atan2(original_conductor.Jc_fit.C1_CUDI1, original_conductor.Jc_fit.C2_CUDI1)

            # Ic = (C1 + C2*B) * (1 - T/Tc0*(1-B/Bc20)^-.59) where only C1 and C2 are unknown - second equation: tan(angle_C1_C2) = C1/C2
            C2 = Ic_cable1 / (1 - Ic_measurements[0].T_ref_Ic / (Tc0 * (1 - Ic_measurements[0].B_ref_Ic / Bc20) ** 0.59)) / (Ic_measurements[0].B_ref_Ic + math.tan(angle_C1_C2))
            C1 = C2 * math.tan(angle_C1_C2)
        elif len(Ic_measurements) == 0:
            # if no measurement is provided use the usual ratio for NbTi superconductors and scale that value by cross section of superconductor and warn the user
            warnings.warn(f'No Measurement for CUDI1 fit provided for coil {coil_name}. Usual ratio for NbTi superconductors of C1 and C2 is used and scaled by cross section of superconductor. Copper-non-copper ratio of magnet model will be used.')

            # check inputs
            if not original_conductor.cable.n_strands: raise Exception('No n_strands specified in modelData of the conductor that should be changed.')
            if not original_conductor.strand.Cu_noCu_in_strand: raise Exception('No n_strands specified in modelData of the conductor that should be changed.')

            # hardcoded values come from magnet "MB inner layer" in csv file "Strand and cable characteristics"
            C1_per_square_meter = 92073.5 / 9.41242e-06   # C1_cab/(Cable Section NbTi) #  = strandArea * nStrands * (1-fCu)
            C2_per_square_meter = -6869.4 / 9.41242e-06   # C2_cab/(Cable Section NbTi) #  = strandArea * nStrands * (1-fCu)
            # NOTE: cab...cable, str...strand, C1_cab = C1_str * nStrands  and  C1_str = C1_str_MB / A_MB * A_thisMagnet

            # scale it with the cross section of superconductor
            strand_cross_section = calc_strand_area(strand_geometry, original_conductor)
            fraction_of_superconductor = 1 - original_conductor.strand.Cu_noCu_in_strand / (original_conductor.strand.Cu_noCu_in_strand+1)
            total_NbTi_area = original_conductor.cable.n_strands * fraction_of_superconductor * strand_cross_section
            C1 = C1_per_square_meter * total_NbTi_area
            C2 = C2_per_square_meter * total_NbTi_area

        # check if values are real and not imaginary (e.g. when Bc20 is bigger than B_ref_Ic)
        if np.iscomplex(complex(C1)) or np.iscomplex(complex(C2)):
            raise Exception(f'When calculating CUDI1 parameters (C1, C2) the values turned out to have an imaginary part. Please check the inputs.')

        return {
            'Tc0_CUDI1': Tc0,
            'Bc20_CUDI1': Bc20,
            'C1_CUDI1': C1,
            'C2_CUDI1': C2,
                }
    else:
        raise Exception(f'No implementation for fit type "{original_conductor.Jc_fit.type}" defined in ParsimConductor.')


def calc_strand_area(strand_geometry, original_conductor):
    if original_conductor.strand.type == 'Round':
        # check conductor type
        if strand_geometry and strand_geometry.type != 'Round':
            raise Exception(f'Type of conductor cannot be changed. Tried to change Round conductor to "{strand_geometry.type}".')

        # if diameter is not changed in conductor database, use the one form modeldata
        if not strand_geometry or not strand_geometry.diameter: diameter = original_conductor.strand.diameter
        else: diameter = strand_geometry.diameter

        # calculate area of circle
        A = np.pi * diameter ** 2 / 4
    elif original_conductor.strand.type == 'Rectangular':
        # check conductor type
        if strand_geometry and strand_geometry.type != 'Rectangular':
            raise Exception(f'Type of conductor cannot be changed. Tried to change Rectangular conductor to "{strand_geometry.type}".')

        # if height/width is not changed in conductor database, use the one form modeldata
        if not strand_geometry or not strand_geometry.bare_height: h = original_conductor.strand.bare_height
        else: h = strand_geometry.bare_height
        if not strand_geometry or not strand_geometry.bare_width: w = original_conductor.strand.bare_width
        else: w = strand_geometry.bare_width

        # calculate area of circle
        A = w * h
    else:
        raise Exception(f'Unknown type of conductor: {original_conductor.strand.type}!')
    return A


# TODO correction factor strand twist-pitch = sqrt(wBare^2+(Lp_s/2)^2)/(Lp_s/2) , where w=wBare cable width, Lp_s=strand twist-pitch; if set to 2, take into account the increases of electrical resistance, ohmic loss per unit length, inter-filament and inter-strand coupling loss per unit length, and fractions of superconductor and stabilizer in the cable bare cross-section due to strand twist-pitch (default=0)
# Resistance_RT = R * L / (f_Cu * A_cond) * f_twist_pitch
# R = C_NIST_fit with the coil_resistance_room_T,  T_ref_coil_resistance and RRR (between 273 and 4))
# search L or f_Cu - set flag what to calculate
# L is coil length and f_Cu from csv file

def Jc_Nb3Sn_Summer_new(T, B, C, Tc0, Bc20):
    if T==0: T=0.001
    if B==0: B=0.001
    frac_T = T / Tc0
    if frac_T > 1: frac_T=1
    Bc2 = Bc20 * (1 - frac_T ** 2) * (1 - 0.31 * frac_T ** 2 * (1 - 1.77 * np.log(frac_T)))
    frac_B = B / Bc2
    if frac_B > 1: frac_B = 1
    Jc = C / np.sqrt(B) * (1 - frac_B) ** 2 * (1 - frac_T ** 2)**2
    return Jc


def Jc_Nb3Sn_Bordini(T, B, C0, Tc0_Nb3Sn, Bc20_Nb3Sn, alpha):
    # Critical current density in a Nb3Sn strand, Bordini fit

    # % % % Check all inputs are scalars or vectors
    if not (np.isscalar(T) or np.isscalar(B) or np.isscalar(C0) or np.isscalar(Tc0_Nb3Sn) or np.isscalar(Bc20_Nb3Sn) or np.isscalar(alpha)):
        if not (len(T) == len(B) == len(C0) == len(Tc0_Nb3Sn) == len(Bc20_Nb3Sn) == len(alpha)):
            raise ValueError('All inputs must be scalars or vectors with the same number of elements.')

    nElements = max([len(T), len(B), len(C0), len(Tc0_Nb3Sn), len(Bc20_Nb3Sn), len(alpha)])

    # % % % Check all inputs are scalars or vectors with the same number of elements
    if ((len(T) > 1 and len(T) != nElements) or (len(B) > 1 and len(B) != nElements) or
            (len(C0) > 1 and len(C0) != nElements) or
            (len(Tc0_Nb3Sn) > 1 and len(Tc0_Nb3Sn) != nElements) or
            (len(Bc20_Nb3Sn) > 1 and len(Bc20_Nb3Sn) != nElements) or
            (len(alpha) > 1 and len(alpha) != nElements)):
        raise ValueError('All inputs must be scalars or vectors with the same number of elements.')

    # Modify the input magnetic field
    B = np.abs(B)
    B[B < 0] *= -1
    B[np.abs(B) < 0.001] = 0.001  # very small magnetic field causes numerical problems

    f_T_T0 = T / Tc0_Nb3Sn
    f_T_T0[f_T_T0 > 1] = 1  # avoid values higher than 1
    Bc2 = Bc20_Nb3Sn * (1 - f_T_T0 ** 1.52)
    f_B_Bc2 = B / Bc2
    f_B_Bc2[f_B_Bc2 > 1] = 1  # avoid values higher than 1
    C = C0 * (1 - f_T_T0 ** 1.52) ** alpha * (1 - f_T_T0 ** 2) ** alpha

    Jc_T_B = C / B * f_B_Bc2 ** 0.5 * (1 - f_B_Bc2) ** 2  # [A/m^2]
    return Jc_T_B


def todo():
    #TODO make functions whereever this function is used
    return None

def make_value_SI(val: float, dim: str):
    if dim in ['mm', 'mOhm', 'mV']:
        return val / 1000
    elif dim in ['m', 'T', 'K', 'Ohm', 'V', '', ' ', '-']:
        return val
    elif dim in ['kA', 'kV', 'km']:
        return val * 1000
    else:
        raise Exception(f'unknown physical unit "{dim}".')
