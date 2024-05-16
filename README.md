# Bachelor Thesis: Visualizing Sequential Rules with Hasse Diagrams

## Overview
This repository contains the code for my Bachelor thesis which investigates the conversion of sequential rules into Hasse diagrams. The objective is to offer a novel visualization method within the partial-order process mining field. By extracting valid, frequent patterns through sequential rule mining and visualizing them with Hasse diagrams, we preserve their inherent order, enhancing the understanding of these patterns.

## Files Description

- `preprocessing.py`:
  - **Purpose**: Preprocesses event logs and adjusts them to a format suitable for the ERMiner algorithm.
  
- `hasseDiagramm.py`:
  - **Purpose**: Converts sequential rules obtained from ERMiner into Hasse diagrams using the GraphViz library.
  ![Hasse Diagram Visualization](https://github.com/LoliSySh/conversion-of-sequential-rules-to-HD/assets/156702881/7adc3093-ad24-4a3f-83ba-2af1385e58ff)

- `analyze_datasets.py`:
  - **Purpose**: Collects statistical characteristics of datasets for further analysis and tests the model's granularity.
- `petrinetz.py`:
  - **Purpose**: Generates Petri nets using various miners provided by the pm4py library to compare these models with the converted Hasse diagram model.


## Requirements
This codebase is developed using Python 3.8. Dependencies include:
- GraphViz
- pm4py

## Contact
For any queries regarding this project, please open an issue in this repository.

## Lizenz

Dieses Projekt steht unter der [GNU General Public License v3.0 Lizenz](LICENSE).
