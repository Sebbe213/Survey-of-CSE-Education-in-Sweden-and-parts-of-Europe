import os
import json
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import openai
from openai_embed import embed_text


def get_all_data():
    data = ["University, Number of students, Percentage of international students"
"Chalmers University of Technology (Sweden), 10.999, 17"
"University of Gothenburg (Sweden), 57.959, 13"
"KTH Royal Institute of Technology (Sweden), 13.955, 26"
"Norwegian University of Science and Technology (Norway), 43.550, 9"
"Universitat Politècnica de València (Spain), 28.000 , 15"
"Gdańsk University of Technology (Poland), 15.622, 7"
"Warsaw University of Technology (Poland), 20.851, 8"
"Politecnico di Milano (Italy), 48.383, 18"
"RWTH Aachen University (Germany), 44.892, 34"
"Technische Universität Berlin (Germany), 33.933, 28"
"Technical University of Munich (Germany), 52.931, 45"
"ETH Zurich (Switzerland), 25.380, 35"
"EPFL (Switzerland), 13.445, 64"
"University of Copenhagen (Denmark), 36.528, 15"
"University of Helsinki (Finland), 31.465, 6"
"university of Cambridge (England), 24.000, 38"
"University of Oxford (England), 26.595, 46"
"University College London (England), 51.058, 54"
"Institut Polytechnique de Paris (France), 10.000, 41"
"Riga Technical University (Latvia), 14.000, 29"
"University of Tartu (Estonia), 15.206, 10",
"""University,Country,Nobel Prizes,Turing Awards,Fields Medals,José Vasconcelos World Award of Education
Chalmers University of Technology,Sweden,0,0,0,1
University of Gothenburg,Sweden,1,0,0,0
KTH Royal Institute of Technology,Sweden,1,0,0,0
Norwegian University of Science and Technology,Norway,2,0,0,0
Universitat Politècnica de València,Spain,0,0,0,0
Gdańsk University of Technology,Poland,0,0,0,0
Warsaw University of Technology,Poland,0,0,0,0
Politecnico di Milano,Italy,1,0,0,0
Rheinisch-Westfälische Technische Hochschule Aachen,Germany,0,0,0,0
Technische Universität Berlin,Germany,0,0,0,0
Technical University of Munich,Germany,3,0,0,0
ETH Zurich,Switzerland,4,1,1,0
EPFL,Switzerland,0,0,1,0
University of Copenhagen (KU),Denmark,4,1,0,0
University of Helsinki (HY),Finland,1,0,1,0
University of Cambridge,England,18,1,4,0
University of Oxford,England,10,3,2,0
University College London (UCL),England,6,0,1,0
Institut Polytechnique de Paris (IP Paris),France,3,0,0,0
Riga Technical University (RTU),Latvia,0,0,0,0
University of Tartu (UT),Estonia,0,0,0,0""",
"""University,Country,Employment Rate (%),Year of Reporting,"Degree Level (UG,PG,PhD)",Time Frame (Months),Scope of Employment Rate,Field Specificity
Chalmers Tekniska Högskola,Sweden,95.3,2024,PG,36,University-specific,STEM
University of Gothenburg,Sweden,79,2024,PG,18,University-specific,STM
KTH Royal Institute of Technology,Sweden,97,2018,PG,24,University-specific,All
Norwegian Univ. of Science & Tech. (NTNU),Norway,98,2022,PG,18,University-specific,All
Universitat Politècnica de València (UPV),Spain,90,2023,UG,0,University-specific,CS/IT
Universitat Politècnica de València (UPV),Spain,94.5,2023,UG,36,University-specific,CS/IT
Gdańsk University of Technology,Poland,80,2019,PG,N/A,University-specific,CS/IT
Politecnico di Milano (Polimi),Italy,97,2024,PG,12,University-specific,All
Politecnico di Milano (Polimi),Italy,91,2024,UG,12,University-specific,All
Politechnika Warszawska (Warsaw UT),Poland,73,2020,PG,N/A,University-specific,CS/IT
Rheinisch-Westfälische Technische Hochschule Aachen (RWTH Aachen),Germany,90,2024,PG,12,University-specific,All
Technische Universität Berlin (TU Berlin),Germany,91,2024,PG,12,University-specific,All
Technical University of Munich (TUM),Germany,95,2024,PG,N/A,University-specific,All
ETH Zurich (Swiss Federal Inst. of Technology Zurich),Switzerland,97,2025,PG,12,University-specific,STEM
École Polytechnique Fédérale de Lausanne (EPFL),Switzerland,94,2020,PG,N/A,University-specific,STEM
University of Copenhagen (KU),Denmark,98.3,2022,PG,N/A,National,STEM
University of Helsinki (HY),Finland,89,2019,PG,12,University-specific,All
University of Cambridge,England,95,2022,UG,15,University-specific,CS/IT
University of Oxford,England,93,2022,UG,15,University-specific,All
University of Oxford,England,95,2022,PG,15,University-specific,All
University College London (UCL),England,75,2022,UG,15,University-specific,CS/IT
Institut Polytechnique de Paris (IP Paris) (Data from École Polytechnique),France,100,2019,PG,6,University-specific,Engineering
Riga Technical University (RTU),Latvia,88,2019,PG,12,National,All
University of Tartu (UT),Estonia,87,2019,UG,6,University-specific,All
University of Tartu (UT),Estonia,94,2019,PG,6,University-specific,All"""]
    return data



def prepare_embedding():
    load_dotenv(Path(".env.local"))
    openai.api_key = os.getenv('API_KEY')
    vector_data = [embed_text(text) for text in get_all_data()]
    with open('embedded_data.json','w') as file:
        json.dump(vector_data, file)
        print("Embedding done!")


prepare_embedding()