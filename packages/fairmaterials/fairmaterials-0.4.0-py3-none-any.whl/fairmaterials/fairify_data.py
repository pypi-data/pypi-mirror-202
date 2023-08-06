import os
import json
import pandas as pd
import sys
from pyld import jsonld

class fairify_data:
    """fairify data  from CSV file and output them as single JSON_LD format file"""

    def find_alt_id(self, key, content, csv_value):
        """
        Find the dictionary containing the alternativeIdentifier in the current context, and update its value.

        Args:
            key (str): The key to look for in the current context.
            context (dict): The dictionary in which to look for the alternativeIdentifier.
            csv_value (Any): The CSV value to use as the value of the "value" key in the alternativeIdentifier.

        Returns:
            bool: Whether the alternativeIdentifier was found and updated.
        """
        if isinstance(content, dict):
            if "alternativeIdentifier" in content and key in content["alternativeIdentifier"]:
                content["value"] = str(csv_value)
                return True
            for sub_dict in content.values():
                if self.find_alt_id(key, sub_dict, csv_value):
                    return True
        elif isinstance(content, list):
            for item in content:
                if self.find_alt_id(key, item, csv_value):
                    return True
        return False

    def json_generate(self, workon):
        """generate valid JSON-LD format output file

        Args:
            workon(list): current processing dataframe

        Returns:
            str: JSON-LD format string
        """
        full_header_str = ""
        full_list = ""
        for i in range(len(self.header)):
            full_header_str = full_header_str + str(self.header[i]) + ","
        for j in range(len(workon)):
            key = self.working_on_key[j]
            value = workon[j]
            if isinstance(value, dict) and 'alternativeIdentifier' in value:
                for alt_id in value['alternativeIdentifier']:
                    if alt_id in self.df.columns:
                        value['value'] = str(self.df.loc[self.row_idx, alt_id])
                        break
            elif 'value' in value:
                value['value'] = str(value['value'])
            full_list += f"{key}:{json.dumps(value)},"

        top_json = '{' + '"@context"' + ':' + str(self.context) + "," + full_header_str + full_list[:-1] + "}"
        top_json = top_json.replace("'", '"')
        return top_json






    def generate_file(self, resultjson, key, sample_id):
        """generate json file with the valid format

        Args:
            count(int or string): current processing dataframe index
            resultjson(string): json ld content after fairified
            key(string): domain for json ld content after fairified
            sample_id(string): sample ID used in the file name
        Returns:
            int: move to next index content
        """
        filename = "{}_{}.json".format(key, sample_id)
        with open(filename, 'w') as f:
            f.write("%s\n" % resultjson)

    def fairify_data(self, data):
        """
        Fairify data from a dataframe or CSV file and process input data into a single JSON-LD file.

        Args:
            data (pd.DataFrame or path): The data to be processed. Either a pandas dataframe or a CSV file path.
        """
        if isinstance(data, str):  # input is a file path
            df = pd.read_csv(data)
        else:  # input is a pandas dataframe
            df = pd.DataFrame(data)

        self.df = df
        initwork_list=self.working_on

        for i in df.index:
            print(i)
            sample_id = str(df.loc[i, 'sampleID'])
            self.row_idx = i
            work_list = initwork_list

            for j in list(df.columns):
                # Look for the key in the current context.
                if j in self.context.keys():
                    for k in range(0, len(self.working_on)):
                        setlist = self.replace(work_list, '$' + str(j), str(df.loc[i, j]))
                        work_list = setlist
                        resultjson = self.json_generate(work_list)
                        findflag = True

                else:
                    findflag = False
                    # First, look for the key in the current context's alternativeIdentifier.
                    alt_id_exists = self.find_alt_id(j, work_list, self.df.loc[self.row_idx, j])

                    if alt_id_exists:
                        print("yes"+j)
                        findflag = True
                        resultjson = self.json_generate(work_list)
                        self.generate_file(resultjson, self.domain, sample_id)
                        # reset domain to user's initial choice
                        self.domain_selection(self.initial_domain)

                        # If not found in the current context, look for the key in other domains.
                    if not findflag:
                        for key, value in self.dic.items():

                            if j in value:
                                print(j)
                                self.domain_selection(key)
                                self.read_data(self.name)
                                print(self.working_on)
                                newwork_list = self.working_on
                                newsetlist = self.replace(newwork_list, '$' + str(j), str(df.loc[i, j]))
                                newwork_list = newsetlist
                                newresultjson = self.json_generate(newwork_list)
                                self.generate_file(newresultjson, key, sample_id)
                                # reset domain to user's initial choice
                                findflag = True
                                #break

                    # If still not found, add the key to the AdditionalProperty section of the JSON-LD.
                    if not findflag:
                        print("Please review the existing keys and reformat if you find a match. "
                              "If you can't find a match, please email us at fairmaterials@gmail.com, "
                              "and we will add it to our template. For now, your key will reside in "
                              "the AdditionalProperty section of the json-ld document.")
                        newdic = {j: {"@type": "propertyValue", "description": "Description of new key",
                                      "value": str(df.loc[i, j]), "unit": "null"}}
                        work_list[-1].update(newdic)
                        resultjson = self.json_generate(work_list)


            self.generate_file(resultjson, self.domain, sample_id)
            self.domain_selection(self.initial_domain)
            self.read_data(self.name)
            # reset domain to user's initial choice


    def replace(self, data, val_from, val_to):

        """replace placeholder with the value inside csv file

        Args:
            data(list or dic):current processing dataframe

            val_from(int or string):value need to be modify

            val_to(int or string):value after modify

        Returns:
            str:dataframe with modified value
        """

        if isinstance(data, list):
            return [self.replace(x, val_from, val_to) for x in data]
        if isinstance(data, dict):
            return {k: self.replace(v, val_from, val_to) for k, v in data.items()}
        return val_to if data == val_from else data

    def read_data(self, name):
        """read json-LD file and spilt them accoording to their header content"

        Args:
            name(string):domain name corresponding to json ld file

        """


        with open(name) as data:
            self.json_data = json.load(data)
            self.context = self.json_data["@context"]
            self.working_on = []
            self.working_on_key = []
            self.header = []
            self.key_list = []
            self.json_data.pop("@context")


        for key, value in self.json_data.items():
            if type(value) == str:
                self.header.append(
                    '"' + str(key) + '"' + ":" + '"' + str(value) + '"' if str(value) is not None else '""')
            else:
                self.working_on_key.append('"' + str(key) + '"')

                self.working_on.append(value)

    def domain_selection(self, domain):
        """
        Domain selection based on user input

        Args:
            domain (string): domain name for fairmaterials
        """
        domains = ['opticalProfilometry', 'streamWater', 'opticalSpectroscopy', 'metalAdditiveManufacturing',
                   'environmentalExposure', 'photovoltaicModule', 'asterGdem', 'sample-metadata',
                   'photovoltaicInverter', 'caryUvVis-instrument-metadata',
                   'capillaryEletrophoresis-Measurement-metadata',
                   'waterMetaDataUSGS', 'spectramaxUvVis-results', 'spectramaxUvVis-instrument-metadata',
                   'photovoltaicCell',
                   'SoilWoSis', 'currentVoltage', 'computedTomographyXRay', 'photovoltaicSystem', 'soil',
                   'diffractionXRay', 'polymerFormulation', 'photovoltaicBacksheet', 'gasFlux',
                   'caryUvVis-results', 'caryUvVis-measurement-metadata', 'polymerAdditiveManufacturing',
                   'spectramaxUvVis-measurement-metadata', 'materials-processing', 'geospatialWell',
                   'buildings', 'capillaryElectrophoresis-calibration-results', 'waterDataUSGS']
        for d in domains:
            if domain == d:
                path = f"./json-ld/{domain}-json-ld-template.json"
                if os.path.isfile(path):
                    self.name = path
                else:
                    print(f"File {path} does not exist.")
                return
        print(f"Domain {domain} not found.")

    def __init__(self, file, domain):
        self.dic = {}
        self.initial_domain=domain
        self.domain = domain
        with open(f"./json-ld/{domain}-json-ld-template.json") as f:
            domain_template = json.load(f)
            self.dic[domain] = list(domain_template["@context"].keys())

        for domain_name in ['opticalProfilometry', 'streamWater', 'opticalSpectroscopy', 'metalAdditiveManufacturing',
                            'environmentalExposure', 'photovoltaicModule', 'asterGdem', 'sample-metadata',
                            'photovoltaicInverter', 'caryUvVis-instrument-metadata',
                            'capillaryEletrophoresis-Measurement-metadata', 'waterMetaDataUSGS',
                            'spectramaxUvVis-results', 'spectramaxUvVis-instrument-metadata', 'photovoltaicCell',
                            'SoilWoSis', 'currentVoltage', 'computedTomographyXRay', 'photovoltaicSystem', 'soil',
                            'diffractionXRay', 'polymerFormulation', 'photovoltaicBacksheet', 'gasFlux',
                            'caryUvVis-results', 'caryUvVis-measurement-metadata', 'polymerAdditiveManufacturing',
                            'spectramaxUvVis-measurement-metadata', 'materials-processing', 'geospatialWell',
                            'buildings', 'capillaryElectrophoresis-calibration-results', 'waterDataUSGS']:
            try:
                with open(f"./json-ld/{domain_name}-json-ld-template.json") as f:
                    domain_template = json.load(f)
                    self.dic[domain_name] = list(domain_template["@context"].keys())
            except json.JSONDecodeError:
                continue
        self.domain_selection(domain)
        self.read_data(self.name)
        self.fairify_data(file)


