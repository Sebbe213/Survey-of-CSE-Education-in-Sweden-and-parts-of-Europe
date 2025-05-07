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
University of Tartu (UT),Estonia,94,2019,PG,6,University-specific,All""",
"""University Name,International Outlook,Industry Income,Source
Chalmers University of Technology (Sweden),77.4,66.0,THE World University Rankings 2023
University of Gothenburg (Sweden),64.4,77.3,THE World University Rankings 2025
KTH Royal Institute of Technology (Sweden),82.9,97.3,THE World University Rankings 2025
Norwegian University of Science and Technology (Norway),66.3,72.3,THE World University Rankings 2025
Universitat Politècnica de València (Spain),57.7,N/A,THE World University Rankings 2025
Gdańsk University of Technology (Poland),39.4,N/A,THE World University Rankings 2025
Warsaw University of Technology (Poland),32.8,54.9,THE World University Rankings 2025
Politecnico di Milano (Italy),64.4,96.3,THE World University Rankings 2024
RWTH Aachen University (Germany),70.3,100.0,THE World University Rankings 2024
Technische Universität Berlin (Germany),N/A,N/A,Not listed in latest THE rankings
Technical University of Munich (Germany),83.1,100.0,THE World University Rankings 2024
ETH Zurich (Switzerland),95.3,84.0,THE World University Rankings 2025
EPFL (Switzerland),95.3,100.0,THE World University Rankings 2025
University of Copenhagen (Denmark),79.3,90.4,THE World University Rankings 2025
University of Helsinki (Finland),59.2,68.2,THE World University Rankings 2025
University of Cambridge (England),97.1,88.4,THE World University Rankings 2025
University of Oxford (England),97.3,99.6,THE World University Rankings 2025
University College London (England),97.7,74.9,THE World University Rankings 2025
Institut Polytechnique de Paris (France),97.0,98.3,THE World University Rankings 2024
Riga Technical University (Latvia),N/A,N/A,Not listed in latest THE rankings
University of Tartu (Estonia),N/A,N/A,Not listed in latest THE rankings
""","""University,Overall Satisfaction,Teaching Quality,Campus Facilities,Support Services,Social Experience
Chalmers Univ. of Technology,90%,90%,85-90%,90%,85%
Univ. of Gothenburg,89%,89%,90%,91%,89%
KTH Royal Inst. of Technology,80%,N/A,N/A,N/A,N/A
NTNU (Norwegian Univ. of Sci. & Tech.),82%,N/A,N/A,N/A,N/A
Univ. Politécnica de Valencia (UPV),88%,N/A,N/A,N/A,N/A
Gdańsk Univ. of Technology,80%,N/A,N/A,N/A,N/A
Warsaw Univ. of Technology (PW),78%,N/A,N/A,N/A,N/A
Politecnico di Milano,86%,N/A,N/A,N/A,N/A
RWTH Aachen University,76%,97%,N/A,82%,N/A
TU Berlin,88%,N/A,N/A,N/A,N/A
Technical Univ. of Munich (TUM),82%,N/A,N/A,N/A,N/A
ETH Zurich (Switzerland),62%,N/A,N/A,N/A,84%
EPFL (Switzerland),N/A,N/A,N/A,N/A,N/A
Univ. of Copenhagen (Denmark),N/A,N/A,N/A,N/A,N/A
Univ. of Helsinki (Finland),N/A,90%,N/A,N/A,N/A
Univ. of Cambridge (UK),91%,90%,94%,84%,75%
Univ. of Oxford (UK),91%,96%,97%,96%,89%
University College London (UCL),80%,N/A,N/A,N/A,N/A
Institut Polytechnique de Paris (France),N/A,N/A,N/A,N/A,N/A
Riga Technical Univ. (Latvia),N/A,N/A,N/A,N/A,N/A
Univ. of Tartu (Estonia),90%,95%,N/A,98%,63%
""","""University,Country,Student-to-Teacher Ratio
Chalmers University of Technology,Sweden,11.1
University of Gothenburg,Sweden,11.5
KTH Royal Institute of Technology,Sweden,15.6
Norwegian University of Science and Technology,Norway,14.8
Universitat Politècnica de València,Spain,15.2
Gdańsk University of Technology,Poland,19.8
Warsaw University of Technology,Poland,10.9
Politecnico di Milano,Italy,24.4
Rheinisch-Westfälische Technische Hochschule Aachen,Germany,37.1
Technische Universität Berlin,Germany,48.2
Technical University of Munich,Germany,41.8
ETH Zurich,Switzerland,15.8
EPFL,Switzerland,12.5
University of Copenhagen,Denmark,4.2
University of Helsinki,Finland,16.5
University of Cambridge,England,11.5
University of Oxford,England,10.8
University College London,England,11.1
Institut Polytechnique de Paris,France,6.7
Riga Technical University,Latvia,31.3
University of Tartu,Estonia,8.6
"""]
    return data



def prepare_embedding():
    load_dotenv(Path(".env.local"))
    openai.api_key = os.getenv('API_KEY')
    vector_data = [embed_text(text) for text in get_all_data()]
    with open('embedded_data.json','w') as file:
        json.dump(vector_data, file)
        print("Embedding done!")


prepare_embedding()