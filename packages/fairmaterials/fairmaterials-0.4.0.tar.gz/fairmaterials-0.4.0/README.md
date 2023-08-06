
![logo](https://i.imgur.com/pqR2OBe.png)

# Fairmaterials
Fairmaterials is a Python 3 package developed by the SDLE Research Center at Case Western Reserve University in Cleveland OH.
We provide here tools used by the Solar Durability and Lifetime Extension Center (SDLE) for FAIRifying data from materials science projects. Functions have been created for numerous tools common in the field in order to make the metadata more Findable, Accessible, Interoperable, and Reproducible.

# Features
 -  Importing JSON template as JSON-LD.
 -   Modify JSON data.
		- Based on CSV file.
		- Based on dataframe file
 -   Output fairiried data as standard JSON-LD format file.
 
#  Setup
1. Install it at bash
```bash
$ pip install fairmaterials
```
2.	Import it in python
```python
from fairmaterials.fairify_data import *
``` 
#  A quick example
***Select a domain and data need to be fairiried***
```python
fairify_data(dataframe,"polymerAdditiveManufacturing")
``` 
***Output will be series of json-ld format file***

#  Versions
All notable changes to this project will be documented in this file.
## [0.4.0] - 2023-04-10
### Added
- Expand the domain to 33 
- Rename domain names
- Fairify data from different domains,data from different domains inside one dataframe(or CSV)can be fairify to different JSON-LD output according to the JSON-LD template. 
- Add synonym function which can fairify data according to the synonym inside JSON-LD template  
#### Domains
-opticalProfilometry
-streamWater
-opticalSpectroscopy
-metalAdditiveManufacturing
-environmentalExposure
-photovoltaicModule
-asterGdem
-sample-metadata
-photovoltaicInverter
-caryUvVis-instrument-metadata
-capillaryEletrophoresis-Measurement-metadata
-waterMetaDataUSGS
-spectramaxUvVis-results
-spectramaxUvVis-instrument-metadata
-photovoltaicCell
-soilWoSis
-currentVoltage
-computedTomographyXRay
-photovoltaicSystem
-soil
-diffractionXRay
-polymerFormulation
-photovoltaicBacksheet
-gasFlux
-caryUvVis-results
-caryUvVis-measurement-metadata
-polymerAdditiveManufacturing
-spectramaxUvVis-measurement-metadata
-materials-processing
-geospatialWell
-buildings
-capillaryElectrophoresis-calibration-results
-waterDataUSGS'

## [0.3.0] - 2023-02-10
### Added
- Expand the domain to 20 
- Rename domain names 
#### Domains
- diffractionXRay
- capillaryElectrophoresis
- polymerAdditiveManufacturing
- photovoltaicModule
- photovoltaicBacksheet
- opticalSpectroscopy
- buildings
- metalAdditiveManufacturing
- opticalProfilometry
- photovoltaicSystem
- computedTomographyXRay
- polymerFormulations
- materialsProcessing
- photovoltaicCell
- photovoltaicInverter
- asterGdem
- environmentalExposure
- geospatialWell
- soil
- streamWater 
## [0.2.0] - 2023-01-10
### Added
- Update fairify_data function,user can select domains to fairify data and dataframe has items from different domains can be fairify into different json-ld file 
- Add new domains into package
#### Domains
- XRD
- CapillaryElectrophoresis
- PolymerAM
- PVModule
- PolymerBacksheets
- OpticalSpectroscopy
- Buildings
- MetalAM
- OpticalProfilometry
- PVSystem
- XCT
- PolymerFormulations
- MaterialsProcessing 
- PVCells
- PVInverter

## [0.1.2] - 2022-12-10
### Added
- Add fairify_data function,user can select domains to fairify data
#### Domains
- XRD
- CapillaryElectrophoresis
- PolymerAM
- PVModule
- PolymerBacksheets
- OpticalSpectroscopy
- Buildings
- GeospatialWell
- MetalAM
- OpticalProfilometry
- PVSystem
- XCT 

## [0.0.213] - 2022-10-8
### Added
- Add template csv file.
## [0.0.212] - 2021-10-7
### Added
- Add group input CSV file generation function.
- Add directly convert a group input CSV file to multiple json file function.
- Add Version part in Readme.md file.

## Funding Acknowledgements:
This work was supported by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable Energy (EERE) under Solar Energy Technologies Office (SETO) Agreement Numbers DE-EE0009353 and DE-EE0009347, Department of Energy (National Nuclear Security Administration) under Award Number DE-NA0004104 and Contract number B647887, and U.S. National Science Foundation Award under Award Number 2133576.