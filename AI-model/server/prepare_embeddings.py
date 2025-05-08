import os
import json
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import openai
from openai_embed import embed_text


def get_all_data():
    data = ["""University, Number of students, Percentage of international students"
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
"University of Tartu (Estonia), 15.206, 10""",
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
""",

"""
Abstract:
Global university rankings are widely used as indicators of institutional quality, yet their
relevance to student priorities remains limited. This study aims to investigate the link
between student-valued educational factors, and the methodologies employed by the most
widely used ranking institutions such as QS, THE and ARWU. A survey was conducted
among students at Chalmers university to identify the parameters they deem most im-
portant when evaluating higher educational quality.""", """Introduction
Computer Science and Engineering (CSE) education faces unique challenges as a rapidly
evolving field where universities must continuously adapt to technological advancements
and changing industry demands. Educational institutions must balance strong theoreti-
cal foundations with practical application, while keeping pace with emerging technologies
and methodologies. In the competitive landscape of higher education today, universities
compete for talented and motivated students on a global stage, particularly so in high-
demand fields such as CSE. Many students, especially those that lack prior contact with
universities, rely heavily on well-known ranking systems to make their university choices
[1]. These university rankings are often used as a measure of institutional quality, but
they present significant limitations. Traditional ranking systems emphasize research out-
put, citation counts, and institutional prestige over teaching quality, student learning
outcomes and industry relevance [2, 3, 4]. This possible disconnect between university
rankings and actual student experience makes it difficult for universities to align their ed-
ucational development with what truly matters to students, presenting a clear challenge
for Chalmers University of Technology and the University of Gothenburg (GU) in their
stated goal to become top CSE educators in Sweden and Europe [5]. There is a strong
need to assess and explore alternative indicators that better reflect what students value
and experience.
By identifying gaps between current ranking systems and student priorities, findings
of this research could potentially contribute to a broader discussion on developing rank-
ing practices that reflect student needs and learning outcomes - leading to a generation
of better prepared computer scientists and engineers. This study will provide faculty at
Chalmers and GU deeper insights into student preferences, allowing them to compare
student perspectives and current priorities of ranking systems. Results of this investiga-
tion can serve as a framework and reference point to ensure that future improvements
are aligned with what truly matters to students.
 
Purpose:
The aim of this study is to investigate how the CSE programs at Chalmers and GU can
strengthen their position as top educators in Sweden and Europe. This is achieved by
understanding how educational quality is currently assessed and identifying which factors
student themselves prioritize when evaluating their educational experience. Through this
comparison, this study seeks to develop an actionable tool that can support Chalmers
and GU to align their strategic development with what students consider most important
in their education.""",
"""Theoretical Background:
Understanding how educational quality is evaluated is crucial to identifying the limita-
tions of existing university rankings and exploring student-centered alternatives. This
section examines the methodologies employed by major ranking systems, highlights their
limitations, explores existing research on student priorities and identifies key indicators
of educational quality that are both commonly used in rankings and valued by students.
Finally, it introduces artificial intelligence, which offers new possibilities for analyzing ed-
ucational data, providing a conceptual foundation for later methodological approaches.

Methodology of Current Ranking Systems:
A variety of methods have been developed to assess educational quality at the institutional
level but the most prominent are international university rankings. The current approach
to evaluating university quality relies heavily on ranking systems that emerged in the early
2000s [6], primarily focusing on research output and academic reputation.
ARWU commonly referred to as the Shanghai Ranking, heavily emphasizes research
productivity and academic prestige [2]. It assigns 40% of its total weight to indicators
related to faculty achievements, such as Nobel Prizes and Fields Medals. Research output,
measured by publications in Nature and Science and citation indices, accounts for an
additional 50%. The remaining 10% is related to teaching quality through the inclusion
of highly cited researchers and award-winning alumni.
The ARWU system largely emphasizes academic excellence; reflected by how the system
prioritizes university research output as well as scholarly accomplishments faculty have
made. It could be argued that the system envisions that university recognition should
heavily weigh on research output. Universities heavily focused on these metrics will, of
course, excel in this ranking system. However, universities with different strengths can
potentially be undervalued. 59% of the total score. These parameters are measured through a combination of cita-
tions, research reputation, research strength, productivity and influence. ”Teaching” is
weighed at 28% evaluating qualities such as teaching reputation, student-to-staff ratio,
doctorate-to-bachelor ratio, doctorate-to-staff ratio and institutional income. The param-
eter ”Industry” measures income from industry partnerships and patents, it is weighed
4%. International outlook is weighed at 7.5% and accounts for international students,
staff and cross-border research collaboration. Despite its broader scope, THE’s method-
ology still prioritizes research output and influence, particularly through citation impact
and academic reputation surveys. The Teaching category includes sub-indicators such as
student-to-staff ratio and doctorate-to-bachelor ratio, which serve as proxies for teaching
quality. However, direct student feedback or learning outcomes are not included. QS bases its evaluation on nine indicators [4]. The most influential metric is Academic
Reputation (30%), and is determined through their own survey. This is followed by Cita-
tions/Research Impact (20%), which measures research impact and Employer Reputation
(15%), reflecting how institutions are viewed by employers. Faculty/Student Ratio (10%)
is used as a proxy for teaching quality. Additional metrics include Employment Outcomes
(5%), International Faculty Ratio (5%), International Student Ratio (5%) and Interna-
tional Research Network (5%) all indicating global reach and collaboration. Finally,
Sustainability (5%) has recently been added, reflecting growing interest in institutional
environmental and social responsibility. QS World University Ranking, like the other
university rankings, favors research productivity and global reputation, with relatively
less emphasis on teaching quality and student experience. All three ranking institutions place a significant portion of their weighting to research-
related parameters. Parameters tied to the student experience are largely absent in
all three ranking systems. Teaching-related parameters, such as faculty-student ratio
and teaching quality, remain secondary to research-related parameters. While ARWU
does include teaching quality, this component is limited to prestigious academic awards
received by alumni. These findings indicate that current global ranking systems do not
emphasize educational quality based on student values. """ ,
"""Limitations of University Rankings:
University rankings are widely utilized by different groups for decision-making. Students
often use rankings to help them choose a university, assuming that higher-ranked insti-
tutions provide better educational and career opportunities [1]. Similarly, universities
use rankings as a benchmarking tool to assess their position relative to peer institutions,
identifying areas for improvement and strategic plans. Additionally, rankings influence
institutional strategies, faculty recruitment, and funding opportunities, reinforcing their
importance in the broader higher education landscape. However, despite their widespread
use, rankings remain a controversial and often misleading measure of educational quality.
The most influential rankings, ARWU, THE and QS, have provided a standardized frame-
work for comparing institutions. However, they have also introduced significant limita-
tions and biases that shape how universities are perceived and operate. These rankings
prioritize research output, often measured by citation counts, journal publications, and in-
stitutional prestige. While research is a crucial function of universities, these rankings fail
to assess the quality of education, student learning outcomes, and teaching effectiveness.
As a result, institutions that focus on pedagogical innovation and student engagement
are often undervalued in global rankings.
Another concern surrounding these ranking systems is their increasing commercializa-
tion, which raises ethical questions about objectivity and fairness. Many ranking or-ganizations offer consultancy services that advise universities on how to improve their
ranking positions [7]. This pay-to-play model creates a conflict of interest, as the same
organizations that evaluate universities also profit from guiding them. Additionally, some
rankings require universities to pay fees for inclusion or for access to detailed reports on
their performance, further privileging institutions with greater financial resources.
This commercialization encourages universities to prioritize ranking-driven strategies [7],
such as increasing research output or hiring highly cited faculty, rather than investing
in teaching excellence, curriculum development, or student-focused initiatives. Conse-
quently, universities that emphasize innovative teaching and student engagement but
lack the financial means to optimize their ranking strategies risk being undervalued in
global comparisons.
The overemphasis on research metrics in university rankings is particularly problem-
atic for technical and applied fields, such as engineering and computer science, where
practical skills, real-world problem-solving, and employer partnerships are crucial. Uni-
versities that invest in innovative teaching methods, interdisciplinary collaboration, and
student-centered learning often find their strengths underrepresented in ranking method-
ologies [8]. Furthermore, rankings tend to favor elite research universities, reinforcing an
institutional hierarchy that does not necessarily reflect the actual quality of education or
the readiness of graduates for industry demands.
Last year, concerns over these issues led the University of Zurich to withdraw from the
THE Rankings [9]. The university criticized the ranking for its emphasis on measurable
outputs, such as the number of publications, which can push institutions to prioritize
quantity over research quality. Additionally, they argued that the ranking failed to cap-
ture the full scope of academic contributions by oversimplifying university excellence into
a set of limited parameters. Another prestigious institution, Utrecht University, also
withdrew from the THE Rankings and QS Rankings [10, 11]. They also share the same
concerns as the University of Zurich about the perverse incentives created by rankings.
They raised issues over the commercial aspects of rankings, in particular how universities
are expected to provide data and fees to maintain their standings.
Chalmers has strong industry collaborations and a focus on applied learning. Unlike
many Swedish universities, Chalmers operates as a private foundation university, giving
it more autonomy in shaping educational strategies. However, despite these advantages,
its global ranking position remains influenced by metrics that do not fully account for
its emphasis on applied education and industry collaboration [12]. As Chalmers seeks to
establish itself as a leader in education, it becomes crucial to critically evaluate existing
ranking methodologies and explore alternative ways to assess and enhance educational
quality.""", """Limitations of University Rankings
University rankings are widely utilized by different groups for decision-making. Students
often use rankings to help them choose a university, assuming that higher-ranked insti-
tutions provide better educational and career opportunities [1]. Similarly, universities
use rankings as a benchmarking tool to assess their position relative to peer institutions,
identifying areas for improvement and strategic plans. Additionally, rankings influence
institutional strategies, faculty recruitment, and funding opportunities, reinforcing their
importance in the broader higher education landscape. However, despite their widespread
use, rankings remain a controversial and often misleading measure of educational quality.
The most influential rankings, ARWU, THE and QS, have provided a standardized frame-
work for comparing institutions. However, they have also introduced significant limita-
tions and biases that shape how universities are perceived and operate. These rankings
prioritize research output, often measured by citation counts, journal publications, and in-
stitutional prestige. While research is a crucial function of universities, these rankings fail
to assess the quality of education, student learning outcomes, and teaching effectiveness.
As a result, institutions that focus on pedagogical innovation and student engagement
are often undervalued in global rankings.
Another concern surrounding these ranking systems is their increasing commercializa-
tion, which raises ethical questions about objectivity and fairness. Many ranking or-
4
ganizations offer consultancy services that advise universities on how to improve their
ranking positions [7]. This pay-to-play model creates a conflict of interest, as the same
organizations that evaluate universities also profit from guiding them. Additionally, some
rankings require universities to pay fees for inclusion or for access to detailed reports on
their performance, further privileging institutions with greater financial resources.
This commercialization encourages universities to prioritize ranking-driven strategies [7],
such as increasing research output or hiring highly cited faculty, rather than investing
in teaching excellence, curriculum development, or student-focused initiatives. Conse-
quently, universities that emphasize innovative teaching and student engagement but
lack the financial means to optimize their ranking strategies risk being undervalued in
global comparisons.
The overemphasis on research metrics in university rankings is particularly problem-
atic for technical and applied fields, such as engineering and computer science, where
practical skills, real-world problem-solving, and employer partnerships are crucial. Uni-
versities that invest in innovative teaching methods, interdisciplinary collaboration, and
student-centered learning often find their strengths underrepresented in ranking method-
ologies [8]. Furthermore, rankings tend to favor elite research universities, reinforcing an
institutional hierarchy that does not necessarily reflect the actual quality of education or
the readiness of graduates for industry demands.
Last year, concerns over these issues led the University of Zurich to withdraw from the
THE Rankings [9]. The university criticized the ranking for its emphasis on measurable
outputs, such as the number of publications, which can push institutions to prioritize
quantity over research quality. Additionally, they argued that the ranking failed to cap-
ture the full scope of academic contributions by oversimplifying university excellence into
a set of limited parameters. Another prestigious institution, Utrecht University, also
withdrew from the THE Rankings and QS Rankings [10, 11]. They also share the same
concerns as the University of Zurich about the perverse incentives created by rankings.
They raised issues over the commercial aspects of rankings, in particular how universities
are expected to provide data and fees to maintain their standings.
Chalmers has strong industry collaborations and a focus on applied learning. Unlike
many Swedish universities, Chalmers operates as a private foundation university, giving
it more autonomy in shaping educational strategies. However, despite these advantages,
its global ranking position remains influenced by metrics that do not fully account for
its emphasis on applied education and industry collaboration [12]. As Chalmers seeks to
establish itself as a leader in education, it becomes crucial to critically evaluate existing
ranking methodologies and explore alternative ways to assess and enhance educational
quality.""",

"""Indicators for Educational Quality:
To provide a more comprehensive assessment, this section explores key indicators that
are widely used by traditional ranking systems as well as being incorporated into our
survey. Having a clear understanding of these metrics are essential for interpreting the
findings of this study.

University reputation:
The reputation of universities is a complex yet important issue. A university reputation
can be described as the collective judgment regarding the quality of the institution.
Building a high quality reputation in the field of higher education requires substantial
time and effort. Having a high reputation impacts the ability of a university to acquire
resources, such as top faculty and students.
Studies suggest that reputation is multifaceted. One of the primary indicators is aca-
demic excellence, which is reflected by quality of research [18]. Some students might
criticize higher education’s emphasis on research output. However, citations and high
quality publications are currently essential in shaping the public’s assessment of a higher
educational institution. Another factor that weighs heavily on university reputation is
how satisfied students are with their experience at the university [19]. Increased stu-
dent satisfaction leads to higher student loyalty meaning that students are more prone
to advocate for, and engage with the university in the future.
International engagement also plays a significant role in shaping university reputation. In-
stitutions that attract international students and staff and participate in research collab-
orations internationally create enriched educational environments that promote broader
perspectives [8]. These global connections establish valuable networking opportunities
that benefit both research activities and the student experience.
Similarly, a university’s relationship with industry contributes substantially to its overall
reputation. Institutions that effectively translate academic research into practical appli-
cations typically generate higher revenue from research projects and industry partnerships
[8]. These connections not only indicate innovation capacity but also create valuable op-
portunities for student internships and improved employment prospects, all factors that
enhance reputation among students and employers alike.

Class Size:
Numerous studies have examined the correlation between class size and its impact on
learning outcomes, academic performance as well as how it affects overall satisfaction
with quality of education.
These findings have important implications for faculty and other decision makers on how
to structure education. The consensus of these studies is clear, larger classes negatively
impact students on multiple measurable metrics [20]. As enrolment increases drastically,
student academic performance declines. Additionally, students also rate their teaching
instructor, learning outcome and overall course experience lower than students attending
courses with a lower student count.
This negative impact is even more pronounced within STEM fields, having a more sub-
stantial negative impact on student grades [21]. A study done in the UK suggests that
students from lower socioeconomic backgrounds are disproportionally affected, impacting
equity within education and STEM. A 2019 study based on the findings of 44 different
STEM courses shows that women are a lot less probable to participate in classes with
student counts above 120 [22]. Other student groups that are also more negatively im-
pacted are first-year students as well as the highest-achieving students. Another study
done based on data collected undergraduate students at a northeastern public university
spanning between 1992 and 2004 state that the effect on student grades is negative across
the board, irrespective of course, gender, ability and minority status [23].
The precise reason for this outcome is difficult to pinpoint, but plausible explanations
that large classes provide reduce opportunities for professors to interact with students,
thereby limiting the ability for students of higher ability get the deeper knowledge they
are seeking as well as for weaker students to get the extra help they need in order to
succeed.

Faculty Acknowledgement:
The presence of highly recognized faculty members, such as those with academic awards,
major journal publications, or acknowledgments from professional associations, is often
regarded as an indicator of educational quality. Research suggests that while faculty
distinctions in research contribute to institutional prestige and knowledge dissemination,
their direct impact on teaching effectiveness and student learning outcomes is less conclu-
sive [24]. The study highlights that faculty with strong research credentials may enhance
graduate-level education by integrating cutting-edge knowledge and critical thinking skills
into teaching, however research excellence does not always correlate with teaching ef-
fectiveness. Furthermore, institutions that prioritize hiring faculty based on research
achievements alone may inadvertently undermine teaching effectiveness, as recognized
scholars may dedicate more time to research activities than to pedagogy.
Given this, faculty research excellence alone cannot serve as a primary metric for as-
sessing educational quality. However, the study highlights that when research is actively
integrated into teaching, particularly at the graduate level, students benefit from ex-
posure to advanced knowledge and analytical skills [24]. This justifies the inclusion of
faculty recognition as a supporting metric in evaluating a university’s educational quality.
A comprehensive evaluation of educational quality should consider both research impact
and pedagogical effectiveness, ensuring that faculty contribute to student learning beyond
research outputs alone.

 Employability:
Employability is a significant metric in university rankings, as it reflects the extent to
which higher education institutions prepare graduates for successful careers. It can be
assessed through employment outcomes (e.g. post-graduation success) and employer
reputation, which captures how industry preceives the value of a university’s graduate.
Research has found that career-focused programs, employer recognition and hands-on
learning lead to higher employability rates, highlighting that a university’s standing in the
job market depends on its teaching methods and curriculum design [25]. The findings also
suggests that curriculum structure and pedagogical methodologies are more influential in
determining job readiness than the state of the job market alone.
Employer reputation is relevant in global university rankings, as it reflects how well uni-
versities align their programs with industry expectations and produce graduates with
relevant skills. Studies highlight that employer reputation is a strong predictor of in-
stitutional success, as it directly influences student employability, industry partnerships,
and university prestige [26]. Universities with a high employer reputation tend to at-
tract more students, increase their funding opportunities, and strengthen collaborations
with businesses, all of which contribute to improved educational outcomes [27]. Em-
ployer engagement in curriculum design plays a significant role in this process, ensuring
that academic programs remain aligned with job market demands. Research has shown
that universities actively incorporating employer input into course structures benefit from
higher job placement rates and enhanced employability [28]. The relationship between
employer reputation and university rankings is evident in statistical models demonstrating
that strong employer perception correlates with higher institutional and enhanced global
standing [27]. Excessive reliance on employer reputation as a measure of educational
quality may result in a disproportionate emphasis on immediate workforce preparation
at the expense of academic development, such as fostering critical thinking, advancing
research, and enhancing faculty expertise [26]. Nonetheless, when balanced appropri-
ately, employability remains a valuable and multidimensional parameter for assessing the
quality of higher education.

 Student Barometer:
Student satisfaction reflects the quality of the learning environment from the students’
perspective and is crucial for identifying areas of improvement. It is positively related to
university performance, financial stability, and the distribution of public funding, with
the most significant effects observed in elite universities and those with high academic
spending [29]. An increase in satisfaction increases institutional reputation, enhances
student loyalty, and results in better rankings, making it more attractive to prospective
students.
Surveys have shown that student satisfaction has a statistically significant effect on uni-
versity applications. For instance, the UK’s National Student Survey (NSS) shows that
student satisfaction has an effect on university applications [30]. Universities with higher
satisfaction levels are more likely to rank higher in the subject league tables and attract
more students. Positive alumni engagement is another benefit of satisfied students, with
such students more likely to donate to their university and participate in various events.
Additionally, satisfied students are likely to donate to their universities and participate
in various events [31]. Positive feedback from alumni about their university is essential
in ensuring the universities know the strengths and weaknesses that can affect their over-
all performance. Finally, the feedback ensures the universities remain relevant to their
alumni and current students [32].
Student satisfaction is normally evaluated with the help of surveys assessing such key
factors as academic quality, teaching performance, administrative services, physical in-
9
frastructure, and social life [33]. Universities analyze this data to identify trends and
prioritize improvements in areas such as the learning environment and student support
services [34]. By systematically analyzing student feedback, institutions can enhance
student experiences and strengthen their competitive standing in the higher education
sector.
3.4.6 Curriculum Design
Curriculum design plays a critical role in shaping the educational quality of higher ed-
ucation programs. A well-structured curriculum ensures that the learning objectives,
teaching methodologies, and assessments are aligned with intended learning outcomes,
which is essential for fostering student achievement and skill development [35]. Curricu-
lum mapping and design serve not only to organize content and sequencing but also to
demonstrate compliance with professional standards and regulatory requirements, mak-
ing it a reliable quality assurance tool [36]. Studies emphasize that curriculum acts as the
foundation linking theoretical knowledge to practical competencies, ensuring that gradu-
ates meet both academic and industry expectations [37]. Moreover, student-centered cur-
riculum models that integrate flexibility, relevance, and experiential learning contribute
positively to student satisfaction, critical thinking and employability [38]. Thus, curricu-
lum design, through its influence on learning outcomes and alignment with accreditation
and industry standards, is a crucial qualitative and quantitative indicator for assessing
the educational quality of CSE programs in higher education.""","""Artificial Intelligence as a Strategic Tool for Educational
Evaluation
Recent advancements in the field of artificial intelligence (AI) have significantly enhanced
the ability to process and generate human-like language, thereby facilitating the devel-
opment of sophisticated tools for research and education. This subsection will present
the foundational concepts of large language models (LLMs), prompt engineering and
retrieval-augmented generation (RAG), all of which form the technical framework for the
AI-assisted chatbot developed in this study. Understanding these technologies is essential
to comprehend how the proposed tool can help Chalmers and GU align their strategic
development with student priorities.
3.5.1 Large Language Models
One of the foundational AI technologies relevant to this study is LLMs, a class of AI mod-
els specifically for natural language processing. These models are neural networks trained
on immense text data to learn patterns and relationships within language, enabling them
to generate human-like text based on given prompts [39]. LLMs learn language patterns
through statistical inference during a process called pre-training. During this phase,
the model is exposed to billions of tokens from diverse sources such as books, websites
and academic papers [40]. This extensive training allows the model to develop a broad
10
understanding of language structure, factual knowledge and basic reasoning capabilities
[41].
In the context of this study, LLMs offer several important advantages. Their ability to
understand natural language queries enables flexible user interaction, while their capacity
to synthesize information across unstructured data sources makes them highly suitable
for analyzing educational quality indicators derived from both institutional documents
and student survey feedback [42]. Their ability to recognize patterns across large datasets
makes them particularly suitable for analyzing educational quality factors from diverse
sources. This makes LLMs particularly valuable for supporting strategic analysis of
educational quality from both institutional and student-centered perspectives.
However, LLMs also present important limitations that must be considered. They can
produce hallucinations, confidently stated but factually incorrect information, particu-
larly when asked about topics beyond their training data [43]. Furthermore, biases present
in the training data can be reflected and even amplified in the outputs, potentially leading
to skewed or ethically problematic results [44]. Additionally, their knowledge is limited to
information available up to their training cutoff date, making them potentially outdated
for rapidly evolving topics [45].
3.5.2 Prompt Engineering
Prompt engineering can be described as the precise crafting of inputs for AI models in
order to maximize output effectiveness [46]. Without precise guidance, AI systems could
possibly struggle to deliver effective and concise results. Today, prompt engineering en-
compasses diverse techniques that can be used to improve the performance of AI models.
Instruction-based prompting, a simple yet powerful technique employs the use of clear
concise goals and directives to the AI model. Direct instructions such as “Summarize”,
“Order” or “Classify” are used in order to establish clear expectations for the AI model’s
output.
Role-based prompting involves instructing the AI to adopt a specific expertise or persona
[47]. For example, when using this technique the idea is to assign the AI a defined
role such as a doctor or historian. This shapes the AI models output in both terms of
knowledge as well as reasoning.
In 2022 researchers at Google introduced a technique called “chain-of-thought” prompting
[46]. This technique has proven to significantly improve the performance of AI models.
When applying this technique the goal is to break down the task at hand into a series
of short to intermediate steps, providing a structured framework for the model to both
minimize errors and make the reasoning of the model more transparent.
In order to achieve the best end results it is often optimal to combine multiple techniques
simultaneously.
11
3.5.3 Retrieval-Augmented Generation
RAG is a method that strengthens the capabilities of large language models, by combining
text generation with information retrieval [48]. Instead of relying only based on a model’s
pre-trained knowledge, RAG retrieves relevant external information before answering a
question, grounding the output in up-to-date, or domain specific data [48].
When a user query is submitted, the system identifies and retrieves the most relevant sec-
tions from a collection of embedded data using cosine similarity metrics [49]. The retrieved
content is the used as contextual input for the language model to generate a response
grounded in factual data, rather than solely on patterns learned during training[50].
This in turn reduces the risk of hallucinated responses, as well as enhancing factual accu-
racy, and provides an efficient method for interacting with structured, or domain-specific
knowledge bases.""" , """Methodology
This study addressed the lack of comprehensive framework that prioritizes the student
perspective by investigating which parameters students consider most important and
comparing these to existing ranking systems.
To guide the investigation, the following key research questions were formulated:
• Which parameters are prioritized by current ranking systems?
• To what extent do current rankings accurately reflect what students find important
in their higher education?
• Which parameters do CSE students at Chalmers and GU find most valuable in
their educational experience?
• How do parameters valued by students, based on student survey, differ from metrics
in current ranking systems?
• What insights can be drawn from the gap between student priorities and traditional
ranking metrics?
To address these questions, an initial literature analysis was conducted to examine the
criteria used by major global ranking systems (ARWU, THE, QS). This was followed by
the design of a survey aimed to identifying student-prioritized parameters.
For comparative purposes, data were collected on selected European universities, pri-
marily focusing on members of the ENHANCE alliance [51], supplemented by other
educational institutions that consistently rank higher and lower in current ranking sys-
tems. This sampling ensured a balanced representation between universities based on
traditional metrics.
12
Subsequent analysis involved weighting the indicators based on student survey responses
and comparing these results against established ranking criteria. Finally, an AI-assisted
analysis tool was developed to facilitate dynamic exploration of the collected data and
to propose a practical mechanism for supporting strategic decision-making within CSE
educational programs.""" , """Task Breakdown
• Existing ranking methodologies:
Examination of how major ranking systems such as ARWU, THE and QS define
and measure university quality. This involves deconstructing each systems method-
ology, identifying the metrics they prioritize, the weighing they employ as well as
the assumptions they have made about metrics that they deem reflect educational
excellence. This analysis will also assess the limitations of traditional systems and
the potential gaps between their approaches and what students place high value on
in their education.
• Surveying:
Several perspectives must be considered when developing a survey to evaluate stu-
dent perspectives on higher education. Allowing students to freely evaluate met-
rics would compromise coherence, instead standardized sets of parameters will be
presented to students, students will rank these according to perceived importance
from high to low. This ensures that the collection of data facilitates comparisons.
Additionally, all survey parameters will be carefully selected based on established
academic literature. Parameters should align with those employed by current rank-
ing systems, allowing for direct comparison between traditional frameworks and
priorities of students.
• Designing an AI-powered tool:
Based upon research findings an interactive platform powered by LLMs will be
created. The system will be developed based on both raw data and synthesized
conclusions to enable the AI-tool to assist in analysing data, generating dynamic and
interactive representations of insights. Rigorous validation will ensure that the tool
produces consistent and reliable answers, aligning with actual results. The platform
will be designed to facilitate both data analysis and tailored reports, allowing the
user to efficiently retrieve customized insights based on their needs. Rather than
creating a custom AI language model from scratch, existing LLMs will be utilized.
4.2 Processes of Literature Work
To ensure that the selected parameters were academically grounded and relevant to higher
education evaluation, a literature review was conducted. The goal was to identify which
parameters have been validated in previous research as significant to educational quality,
particularly within technical and engineering disciplines.
The process became exploratory in nature, given that educational quality in computer sci-
ence and engineering is not a well-established field with universally agreed-upon method-
13
ologies. As such, the literature review extended beyond CSE to include research from
broader fields such as general higher education, engineering education, business, and
education policy. This broader scope was necessary to capture diverse perspectives on
quality assessment and to identify transferable evaluation frameworks applicable to CSE
education. Academic sources were identified using keyword-based searches in databases
such as Elsevier-owned databases (Scopus and ScienceDirect), SpringerLink, and Google
Scholar. Search terms including combinations of ”educational quality indicators”, ”higher
education quality”, ”university ranking”, ”assessment of educational quality” etc.
Additionally, the AI-assisted tool Scopus AI was used to explore research questions in
natural language, such as “What indicators are used to evaluate educational quality in
higher education?”, ”How does parameter X affect educational quality?”, “What indica-
tors matter most in university rankings?” etc. Scopus AI provided summerized insights
based on Scopus-indexed literature, which were manually reviewed for relevance.
Highly cited, peer-reviewed or recently published papers were prioritized, in order to bal-
ance scholarly impact with relevance. Studies were included if they contributed empirical
or theoretical insights into educational quality indicators. This interdisciplinary approach
allowed for the identification of parameters used in the data collection and data analysis.""" , """Collecting Data with AI-assisted Scraping
To ensure the collect of consistent and comparable data for our analysis, data collection
was relied exclusively on AI-assisted methods using LLMs and prompt engineering rather
than traditional scraping frameworks like Scrapy or Selenium. This approach allowed us
to efficiently extract and validate information from a wide range of sources without build-
ing manual scrapers. Additionally, this method allowed us to scale the data collection
process across multiple universities across Europe while ensuring adaptability to various
languages, web formats and content structures. Building manual scrapers for each indi-
vidual site would have required extensive resources and technical customization, which
would not have been feasible within the project’s scope and timeline.
The following LLM platforms were utilized for the data collection process:
• ChatGPT 4o Deep research
• DeepSeek R1
• Grok
• Perplexity
• Gemini
These models were selected for their advanced natural language understanding, web-
integrated capabilities, and versatility in handling structured prompts.
The data collection process incorporated a triangulation strategy. This meant prompting
multiple LLMs with the same query and comparing their responses. Doing this, ensured
14
prompt clarity by observing how different models interpreted the same task. Also, enabled
cross-validation of results to identify inconsistencies or hallucinations and improving the
reliability and objectivity of data collected.
To ensure consistency and maximize the relevance of the AI responses, a structured
prompt engineering framework was developed consisting of the following principles.
• Be specific - Include constraints and disclaimers.
• Always include a goal - Establish a clear output.
• Role-based prompting - The model has the persona of a research expert.
• Include examples for clarity - Provide examples of how data should be presented.
The adoption of AI-assisted scraping combined with prompt engineering was essential
for overcoming practical challenges such as time constraints, language barriers, and data
heterogeneity across European universities.
Scraping publicly accessible data raises important legal questions regarding copyright and
intellectual property rights. Under EU law, particularly Directive 96/9/EC on database
protection, scraping data from publicly accessible websites is generally permissible pro-
vided the following criteria are strictly observed:
• The data collected is publicly accessible without bypassing any authentication or
security measures.
• Scraping activities respect each website’s robots.txt file, terms of service, and ex-
plicit copyright statements.
• Data extraction avoids protected databases, such as those specifically compiled by
commercial or proprietary means unless explicitly authorized.
This project strictly followed to these standards. Data collection respected the boundaries
defined by websites’ robots.txt files. By adhering to these legal guidelines, the project
ensures ethical and compliant data collection that respects intellectual property rights.
The AI-models were prompted to extract information primarily from official univsersity
websites, annual reports, global university ranking platforms (e.g., ARWU, QS, THE),
public eduction statistics from government databases. Non-academic or user-generated
content such as blogs and forums was exluded through prompt constrains.
The AI-assisted data collection for student barometers and student statisfaction surveys
conducted by universites yielded very limited data. During the manual validation, many
of these datasets were either not publicaly available or restricted behind authentication
portals. To address the missing data, we proceeded to contact all the universities whitin
our scope (excluding Chalmers and GU) directly via email, requesting access to their
most recent student barometer or internal student survey results, if available. Only six
universities responded, among these:
15
• KTH responded they do not have much on this subject, but provided a link to their
mid-program survey. Last one conducted was in 2019.
• ETH Zurich confirmed a 2024 student satisfaction survey had been conducted but
the results were not yet published. Results from a previous survey from 2019 was
shared instead.
• TUM declined to share data due to institutional data protection policies.
• UCL also declined to share their internal survey results due to authorization re-
strictions, as access is limited to internal university affiliates.
• RWTH Aachen provided a public link to institutional student survey results from
2022.
• NTNU responded they do not have data on this subject.
Due to the inconsistent availability and limited access to student barometer data, only
partial integration of this metric was possible. The lack of standardized reporting and
open access across institutions restricted the scope of comparison for this particular in-
dicator.
All prompt-response were saved as CSV file, including the promts and LLM source. This
to ensure traceability and reproducibility of the scraping process. This also allowed
the team to revisit, audit or revise entries as needed and ensure transparency in the
methodology.""" , """Mathematical Methodologies for Data Processing
To enable meaningful comparisons across universities and parameters with different units
and scales, all quantitative data was standardized using z-score normalization. The z-
score for a given value xi was computed using the formula:
zi = xi − μσ
where μ is the mean and σ is the standard deviation of all values for a given parameter.
This transformation centers each parameter distribution around zero and normalizes the
variance, allowing direct comparison between the parameters.
To make the result more interpretable and consistent with a [0,1] scale, the z-score were
then converted into cumalitve distribution function (CDF) values using standard normal
distribution. This was calculated as:
Scorei = Φ(zi)
16
where Φ(zi) is the CDF of the standard normal distribution. This conversion reflects
the relative standing of each university within the dataset, where values closer to 1 indi-
cate stronger performance and values near 0 indicate weaker performance for the given
parameter.
For parameters where lower values are preferable (e.g., student–teacher ratio), the result-
ing CDF scores were inverted using:
Adjusted Scor_ei = 1 − Φ(zi)
This ensured that, across all metrics, higher scores consistently represented better per-
formance.""" , """"Development of the Student-Centered Ranking Model
A student survey was conducted with 108 respondents, who rated the importance of eight
educational quality indicators on a scale from 1 to 8. The final parameters included in the
model were: Teaching Quality, Employability, University Reputation, Support Services,
Campus Facilities, Social Experience, Faculty Acknowledgement, and Class Size. The
average rating for each parameter was normalized so that the combined weights summed
to 1. These weights served as the basis for evaluating university performance from a
student-centered perspective.
For four of the parameters (Teaching Quality, Campus Facilities, Support Services, and
Social Experience) there were significant gaps in available data. In these cases, dummy
values were applied, estimated by considering the range between known maximum and
minimum values for that parameter and making a reasoned approximation. While this
introduces a margin of error, it allowed for a complete ranking of all universities included
in the study. Due to the qualitative nature of curriculum data, and difficulties in con-
sistently extracting it across institutions and languages, the curriculum parameter was
excluded from the final ranking model, despite being rated highly by students. This
decision was made to preserve fairness and consistency across all evaluated universities.
To compare these results with existing evaluation systems, an average rank was calculated
from each university’s position in three major global ranking systems: ARWU, THE and
QS. These average ranks were normalized using z-scores and transformed into CDF scores,
allowing the generation of a comparable 1–21 scale.
While this approach provides a novel student-informed perspective on educational quality,
it is not without limitations. The inclusion of dummy values introduces some estimation
bias, and the exclusion of curriculum as a parameter limits the model’s ability to reflect
certain pedagogical aspects. Nonetheless, this model demonstrates the potential of in-
tegrating student preferences into university evaluation systems, offering an alternative
lens to complement traditional global rankings.
17""",
"""4.6 Implementation of the AI-bot
To strengthen the connection between the findings and the research objective, an AI-
assisted tool was developed. The purpose of this tool is to allow dynamic interaction with
the collected data, enabling users to explore patterns, validate findings, and investigate
aspects of educational quality that students identified as important.
The AI-model has been built with the help of Open-AI’s API. This allows us to use some
of the best available pre-trained models on the market at a low cost.
When creating a RAG, there are a few steps to consider in order to get good performance.
There may be a temptation of simply providing all the data in the prompt. That is a
simple and straight forward approach but with major drawbacks. Firstly, the prompt
becomes very large, leading to high input costs from the API. Secondly it becomes harder
for the model to identify relevant data, increasing the chances of poor responses. In the
context of this project, accuracy and cost performances are essential. Inaccurate responses
could lead to the user getting a distorted understanding of university data, performance
and student needs. High operational costs will limit the tools accessibility across faculty.
Prioritizing cost and performance is therefore crucial in ensuring the creation of a reliable
tool that can be used by all stakeholders.
Instead, the technique should involve the usage of embedded models, careful prompt
engineering and data partitioning.
Step one is to initiate your embedding models. An embedding model is a model that
converts text, images and audio into floating-point numbers. These numbers are based on
training and assigned using mathematical formulas. The number represents coordinates
in a vector space which is usually hundreds of dimensions which is too complex for the
human mind to envision [52]. A large number of dimensions are needed to be able to
capture all the slight nuances that come with text, pictures, etc. In theory, the closer the
coordinates of two data points are the more related they are. However, small differences in
some of the dimensions can lead to large distances between the vectors giving a misleading
picture.
This implementation consisted of using one of Open-AIs pre-trained embedding models,
specifically ”text-embedding-3-small”. This model, while the smallest provides a good
balance between cost and performance scoring very close to the larger ones [53]. The
model receives the data stored as separate chunks in a simple array. Once the model
finishes processing, all the embeddings get stored in a JSON file for repeated use.
If the embedding model does not give us a true similarity what should we use? A common
approach is to use the cosine-similarity formula:""","""The formula considers the angle between the vectors. A smaller angle means the vectors
are pointing in the same direction indicating a stronger relationship. The values ranges
from [-1,1], the closer the value is to 1 the higher the similarity.
An easy way to understand this is by imagining two cars. The cars are parallel to each
other but move in opposite direction. They have many things in common but ultimately
reach different destination. Similarly, two phrases could be formulated and structured in
the same way but mean completely different things.
This technique allows users to ask complex questions allowing for a deeper understanding
of the research and topics regarding it. It also unlocks a freedom for the stakeholders such
as university administrators, researchers and students to explore issues not answered in
this report. This supports our broader goal to provide a tool that helps the faculty to
identify, understand and act on the factors that contribute to high quality education.
Before using the formula, we must embed the users prompt. Then in a loop, all embed-
dings from the data are compared with the prompt using cosine similarity. The three
chunks of data with the highest scores are then given to the AI followed by the users
question.
Step two is to implement the AI-model itself. The model was also using OpenAI’s API,
specifically ”gpt-3.5-turbo”. For these models to function correctly you need to define so
called roles. Roles are a built in future that allows developers to give different prompts
to the AI based on specific situations.
Arguably, the most important role is the so called system. You need to apply careful
prompt engineering in order to make the model understand how it should behave. In this
project was the prompt designed to ensure that the model delivers factual and relevant
relevant responses. This is particularity important when dealing with topics regarding
education. By defining the tone and scope of the models answers, prompt engineering
plays an important role in making the tool useful for exploring what makes a successful
university.
Lastly, it is important to partition your data so that the model does not receive to little
or to much information. Each element in the array is a chunk, and each chunk should
contain related information. The strategy that got applied for this bot is that each chunk
is either a table or a related piece of information. The idea is to give the model as
little information as possible but enough to answer the questions correctly. Again, this
minimizes cost and boosts performance.
The next critical step was implementing the server infrastructure and wiring it with the
frontend design to provide an integrated and user friendly interface. For this purpose,
Flask was selected, a lightweight Python web framework, due to its simplicity, scalability,
and ease of integration with AI libraries. The server plays a central role in handling all
user interactions and acts as a mediator between the frontend interface and the RAG-
based AI model. When a user enters a question in the frontend application, this request
is sent directly to the Flask server via HTTP API calls. The server processes this request
by first converting the user’s question into numerical representations using the embedding
model. It then applies cosine-similarity measures to retrieve the most relevant data from
19
our stored knowledge base, which is subsequently passed to the OpenAI GPT model.
The GPT model generates an answer, which the server sends back to the frontend as a
structured response in JSON format.
Integration between the server and frontend design was carefully structured through
clearly defined Restful API endpoints. Each endpoint is designed to handle specific
tasks, such as submitting user queries and fetching answers. This modularity in design
facilitates easy debugging, testing, and potential future scalability. The frontend, built
with React and TypeScript, consumes the server’s API responses dynamically, updating
the user interface in real-time without requiring page refreshes. This seamless integration
ensures a smooth and responsive interactions with the AI-bot, significantly enhancing
usability and overall satisfaction.
Through this approach, the AI-assisted tool was designed to serve multiple research-driven
functions:
• Stakeholder engagement: Providing a platform for faculty and administrators
at Chalmers and GU to query the data in a manner aligned with student-centered
indicators.
• Support for strategic work: Offering faculty members a proposed tool to inter-
act with and interpret student-centered data, facilitating evidence-based decisions
aimed at enhancing the strategic development of educational offerings.
• Scalability for future development: Establishing a framework for future up-
dates, including the integration of new universities or updated datasets, to contin-
uously align with evolving student needs.""","""Results
This section presents the findings of the study based on the student survey, the com-
parative analysis between student priorities and global ranking metrics, and the devel-
opment of the student-centered ranking model. The results highlight the parameters
students value most, the observed discrepancies between student preferences and tradi-
tional ranking systems, and the resulting shifts in university rankings when applying a
student-centered evaluation.
5.1 Student-Preferred Educational Quality Indicators
To better understand what students themselves consider important when evaluating the
quality of education, a survey at Chalmers (n = 108) was conducted, asking students to rate various
parameters on a scale from 1 (least important) to 8 (most important).According to the result of the survey, the most highly valued parameters were Teaching
Quality (mean = 6.79), Employability (mean = 6.67) and Curriculum (mean = 6.35).
These were followed closely by University reputation (mean = 5.75) and Support Services
(mean = 4.73) and Campus Facilities (mean = 5.60). By contrast, parameters such as
Faculty Acknowledgement (4.55), Social Experience (5.75), and Class Size (3.11) were
rated as less important by students.
At the end of the survey, students got the option to suggest other parameters that they
considered important, that were not mentioned in this survey. Out of 108 respondents,
15 students provided suggestions for other parameters. Location was mentioned most
frequently, this also includes accessibility to transportation and living situation. Other
21
factors like review from graduated students and drop-out students, safety, inclusion, food
options, expected salary and personal finance were also mentioned, indicating further
areas of interest not captured by the core parameters.
This distribution suggests that students place the greatest value on academic outcomes,
such as the quality of teaching, the practical utility of the education in terms of job
readiness and the structure and content of the curriculum, rather than on reputation-
based or environmental factors. These findings underscore the need to re-evaluate current
educational assessment models that heavily weight research and prestige, potentially at
the expense of direct student learning outcomes.""",

"""Comparison of Global University Rankings and Student-Centered Ranking
To enable a consistent comparison across the major global university rankings, each
university’s position in the ARWU, THE and QS ranking systems was retrieved. Because
the original rankings span different ranges and criteria, we re-ranked the 21 universities
in our scope from 1 to 21 within each system, where rank 1 represents the highest global
position among the selected universities. This allows for a more intuitive comparison and
aligns the external rankings with the format used in our CDF-based model.""",

"""
Ranking is from ShanghaiRanking:
Rank,University,World Ranking (ARWU)
1,Highly prestigious University of Cambridge,4
2,University of Oxford,6
3,University College London,16
4,ETH Zurich,21
5,University of Copenhagen,32
6,Technical University of Munich,47
7,École polytechnique fédérale de Lausanne,55
8,University of Helsinki,99
9,University of Gothenburg,101–150
10,Norwegian University of Science and Technology,151–200
11,Kungliga Tekniska Högskolan,201–300
11,Politecnico di Milano,201–300
11,Rheinisch-Westfälische Technische Hochschule Aachen,201–300
11,Technische Universität Berlin,201–300
15,Institut Polytechnique de Paris,301–400
16,Chalmers Tekniska Högskola,401–500
16,Riga Technical University,401–500
18,Universitat Politècnica de València,601–700
19,University of Tartu,601–700
20,Gdańsk University of Technology,801–900
21,Warsaw University of Technology,901–1000""",

"""Ranking from Times Higher Education:
Rank,University,World Ranking (THE)
1,University of Oxford,1
2,University of Cambridge,2
3,ETH Zurich,4
4,Technical University of Munich,14
5,École polytechnique fédérale de Lausanne,20
6,University College London,34
7,Institut Polytechnique de Paris,42
8,Rheinisch-Westfälische Technische Hochschule Aachen,60
9,Technische Universität Berlin,65
10,Kungliga Tekniska Högskolan,69
11,Politecnico di Milano,88
12,Chalmers Tekniska Högskola,126–150
12,University of Copenhagen,126–150
14,Norwegian University of Science and Technology (NTNU),176–200
14,University of Helsinki,176–200
14,Warsaw University of Technology,176–200
17,University of Tartu,301–400
18,Universitat Politècnica de València,401–500
19,University of Gothenburg,501–600
20,Gdańsk University of Technology,801–1000
20,Riga Technical University,801–1000""",

"""Ranking from QS World University Rankings:
Rank,University,World Ranking (QS)
1,University of Oxford,2
2,University of Cambridge,4
3,ETH Zurich,7
4,École polytechnique fédérale de Lausanne,10
5,Technical University of Munich,19
6,Politecnico di Milano,23
7,University College London,29
8,Kungliga tekniska högskolan,37
9,Institut Polytechnique de Paris,38
10,Technische Universität Berlin,45
11,Rheinisch-Westfälische Technische Hochschule Aachen,106
12,Chalmers Tekniska Högskola,112
13,Norwegian University of Science and Technology (NTNU),134
14,Universitat Politècnica de València,145
15,Warsaw University of Technology,194
16,University of Copenhagen,297
17,University of Helsinki,358
18,Gdańsk University of Technology,348
19,University of Tartu,358
20,Riga Technical University,451–500
21,University of Gothenburg,501–550
""",
"""Ranking created by the writers (bachelor students) based on a student centric model: 
Name of University,Student Ranking,Average Rank Change in comparison with traditional ranking
University of Oxford,1,1,+0
University of Cambridge,2,2,+0
Chalmers Tekniska Högskola,3,15,+12
ETH Zurich,4,3,-1
Universitat Politècnica de València,5,16,+11
University of Gothenburg,6,17,+11
University of Helsinki,7,14,+7
University of Copenhagen,8,11,+3
NTNU,9,13,+4
EPFL,10,6,-4
IP Paris,11,12,-1
Riga Technical University,12,20,+8
Technical University of Munich,13,4,-9
Politecnico di Milano,14,8,-6
KTH,15,7,-8
University College London,16,5,-11
Technische Universität Berlin,17,9,-8
RWTH Aachen,18,10,-8
University of Tartu,19,19,+0
Warsaw University of Technology,20,18,-2
Gdańsk University of Technology,21,21,+0

Table above presents the ranking of 21 European universities based on a student-centered
weighting model. The rankings were computed by applying weights derived from a stu-
dent survey, reflecting the parameters students find most important when assessing edu-
cational quality.
26
The comparison reveals noticeable differences between the traditional rankings and the
student-centered ranking. Out of 21 universities, eight universities improved their posi-
tion in the student-centered ranking compared to their average global rank.
The most significant improvements was observed for Chalmers (+12), GU (+11) and Va-
lencia Polytechnic University (+11) in the student-centered ranking compared to their av-
erage global ranking. This suggest strong performance in parameteres valued by students.
Four universities remained in the same position. University of Oxford and University of
Cambridge held their positions at the top of the ranking, while the University of Tartu
and Gd´ansk University of Technology remained at the bottom. Nine universities dropped
in ranking in the student-centered ranking compared to their average global ranking. The
largest declines were observed for UCL (-11), Technical University of Munich (-9), KTH
(-8), RWTH Aachen (-8) and Technische Universit¨at Berlin (-8).
""",
"""
Discussion:

The results of this study highlight a clear disconnect between what students value in their
educational experience and what current university ranking systems prioritize.
The student survey results indicated that the most important parameters for students
were teaching quality (mean = 6.79), employability (mean = 6.67) and curriculum design
(mean = 6.35). These were followed by faculty acknowledgement, support services and
campus facilities. On the other hand, parameters such as university reputation, class
size and international outlook were rated as less important. These results suggest that
students prioritize direct educational experiences and career-relevant outcomes above
research output or institutional prestige.
In contrast, our analysis of major university rankings (ARWU, THE, and QS) revealed a
predominant focus on research metrics and institutional prestige. All three ranking sys-
tems place their highest emphasis on research-related parameters. The ARWU allocates
90% of its weight to research impact and faculty acknowledgment, leaving only 10% for
teaching quality. Similarly, THE designates 57% to research impact, 29% to teaching-
related indicators, and does not include curriculum or employability as direct metrics.
QS assigns 50% to academic reputation and research citations combined.
Parameters such as curriculum design, student support and teaching quality, which were
highly valued by students, are either absent or receive low priority in all three ranking
systems. Meanwhile, parameters that student rated as less important, such as research
citations and academic reputation, dominate these ranking methodologies. These findings
confirm previous observations that university rankings are primarily designed to measure
research excellence rather than educational quality.
This comparison highlights a clear gap between what students consider important for educational quality and what global university rankings prioritize. While there is some
partial alignment (e.g., QS’s inclusion of employability metrics see figure 3), many
student-valued aspects are underrepresented in current ranking frameworks.
For Chalmers and GU to achieve their strategic aim of becoming ”top educators” in Swe-
den and Europe, our findings suggest that traditional ranking positions should not be
the primary measure of success. The disconnect identified in this study calls for alterna-
tive models of assessing educational quality. While traditional rankings serve important
purposes in evaluating research output, they fail to capture the multidimensional nature
of educational quality. The findings of this study contribute to the growing critique of
global university rankings as comprehensive measures of institutional quality. Recent
withdrawals from rankings by prestigious institutions like the University of Zurich and
Utrecht University reflect increasing concern about the perverse incentives created by
rankings and their failure to capture educational quality accurately. For technical fields
like CSE, where practical skills and industry relevance are particularly important, the
limitations of research-focused rankings are especially pronounced. This suggests a need
for discipline-specific approaches to quality assessment that account for the unique char-
acteristics and requirements of different fields.
The student-centered ranking model developed in this study offers a valuable alternative
perspective, providing a framework for evaluating educational quality based on student
priorities rather than solely on research metrics. By weighting universities according to
the factors students value most, such as teaching quality, employability, and support
services, the model offers a fundamentally different perspective compared to traditional
global rankings, which primarily focus on research output and institutional prestige. Our
results demonstrate that universities which align more closely with student priorities can
achieve higher rankings in the student-centered model, even if their traditional global
rankings are modest.
The student-centered ranking model also offers a framework for ongoing strategic evalu-
ation. By updating the model with student input, Chalmers and GU can continuously
monitor how well their educational offerings align with evolving student expectations,
ensuring sustained leadership in CSE education in Sweden and Europe. """,

"""
Our-developed-tool to support strategic decision-making:
The AI-assisted tool developed as part of this study serves as a practical mechanism
to support strategic decision-making aligned with student priorities. By enabling dy-
namic exploration of student-centered educational data, it allows faculty, administrators,
and other stakeholders to investigate specific areas for improvement, validate hypotheses
about educational quality, and explore how their institutions perform relative to student
expectations. In this way, the tool can help Chalmers and GU to align their educational
strategies more closely with what students value, rather than relying solely on traditional
ranking metrics.
However, while the AI tool offers promising capabilities, it is important to acknowledge
its limitations. The system depends on the quality and scope of the underlying data,
which in this project was constrained by availability, particularly regarding student sat-
isfaction metrics. Additionally, the tool relies on pre-trained LLMs, which can introduce
risks such as hallucinated outputs, biases inherited from training data, or misinterpreta-
tion of nuanced educational factors. Although the RAG architecture help some of these
28
risks by grounding responses in structured data, it cannot entirely eliminate them. Fur-
thermore, the current version of the tool focuses primarily on the initial dataset collected
for this study and may require significant updates or retraining to remain relevant as
educational priorities and institutional strategies evolve. Thus, while the AI-assisted tool
represents an important step toward data-driven, student-centered strategic development,
it should be viewed as a complementary support system rather than a definitive evalua-
tor. Continuous refinement, critical oversight, and integration with broader institutional
decision-making processes are essential to fully realize its potential impact.""",

"""Limitations:

The survey provided a wealth of data regarding student priorities, but encountered several
limitations. The forced ranking method over simplified decision-making, while minimal
response rate to our open-ended question significantly limited our ability to gather qual-
itative feedback. Feedback we did receive highlighted missing parameters and a lack of
clarity regarding their specifications. Self-selection bias and convenience sampling used in
this survey may not accurately reflect the broader student population. The narrow focus
of the survey also provided limited insight into why respondents ranked the options as they
did. Future surveys should aim to include a more diverse sampling approach, incorporate
both closed and open-ended questions, and employ improved strategies for engagement
strategies to ensure student perspectives are more comprehensibly represented.
The scope of this study developed gradually, beginning with exploratory work to define a
clear research direction. Our initial ambition was to construct a new university ranking
system based on student-centred parameters and develop an AI-based product informed
by our findings. However, we soon realized that developing a comprehensive and mean-
ingful ranking is methodologically complex and resource-intensive, particularly given the
high number of technical universities across Europe.
As the project evolved, we refined our focus toward analysing existing universities to
uncover the factors behind their success. The goal shifted toward providing actionable
suggestions for Chalmers and the University of Gothenburg (GU). From the outset, it
was apparent that international rankings tend to prioritize research output while often
neglecting the student learning experience.
Selecting relevant parameters, and justifying the inclusion, proved challenging due to
differing viewpoints within our group. Determining appropriate weights of parameters
and balancing qualitative elements with quantifiable data added further complexity.
We faced limitations in choosing which universities to include in our comparison. Data
inconsistencies were a major obstacle, particularly when relying on national student sur-
veys, which varied greatly in structure and availability. These datasets were often times
not available to anyone outside the respective institutions. The lack of standardized met-
rics for key qualitative aspects required us to use proxy indicators. Finally, we had to
narrow the scope of our analysis, such as deciding whether to include only Computer
Science programs, or broader categories like Computer Science and Engineering (CSE),
which further constrained our comparisons.


Future Work: 
This thesis highlighted several limitations and areas where further research could add
valuable insights. One major challenge was obtaining relevant data, especially from the
student surveys. The available datasets were often limited in scope or lacked the depth
needed to draw meaningful conclusions about student priorities and perceptions. Future
research should aim to design and conduct more targeted surveys, as outlined in 6.2.2,
to capture more relevant and actionable feedback from students.
Additionally, this study relied heavily on recent data, which restricts the ability to ana-
lyze long-term trends. A longitudinal approach, for example, over a 10-year span, could
provide a deeper understanding of how university rankings evolve over time, and how
changes in strategy or external factors influence performance. Another important aspect
that was beyond the scope of this thesis is how students, faculty, and other stakeholders
perceive and interpret the indicators used in major rankings. Understanding these per-
spectives could shed light on whether current metrics align with the values and priorities
of the academic community.
There is also potential for improved collaboration and data sharing between universities.
Stronger partnerships could lead to more transparent and standardized datasets, making
comparative analysis more robust and meaningful. It would be particularly interesting to
explore how increased transparency and openness could impact the perception and utility
of rankings, both internally at a university level, and in the wider academic landscape.""",
"""Social and Ethical Aspects
This project addresses societal and ethical considerations both regarding the student-
centered ranking and the development of the LLM-based chatbot. The aim of this project
was to propose alternative indicators for evaluating educational quality based on student
preferences, this has potential societal benefits by offering universities insights into how
they might better align education with student expectations.
This project did rely solely on public data sources, anonymized survey responses and
data processing. However, the use of dummy values for missing data introduced a risk
of reduced accuracy. Transparent communication of data limitations have been clearly
disclosed, to avoid misleading conclusions and to respect the integrity of the analysis.
In developing the chatbot, specific ethical consideration arise. LLMs are known to be
susceptible to reproducing biases present in their training data [54]. Additionally, studies
show that even the way prompts are phrased can influence outputs and potentially inject
bias [55]. Although this project uses RAG focused on controlled project-specific data,
there remains a general risk that the chatbot could misrepresent or oversimplify complex
information. Recognizing this, users are advised that the chatbot should be seen as an
exploratory tool rather than a definitive evaluator.
Another aspect is fairness and inclusivity. Research shows that LLMs trained predom-
inantly on data from Western contexts may insufficiently represent diverse educational
30
perspectives [55]. Although this project is limited to European universities, this was
a conscious choice to ensure manageable data collection within the project’s scope and
timeline. The methodology was designed to be scalable, allowing future expansion to
universities globally once the minimum viable product has been validated.
From an environmental perspective, the project has negligible impact. All activities
were conducted digitally, using pre-trained AI models for inference rather than resource-
intensive retraining, and no significant computational resources were consumed beyond
standard academic levels.
Overall, the project promotes societal benefit by encouraging a more student-centered
perspective on educational quality. Ethical risks, such as bias amplification and data
handling limitations, have been minimized through careful methodology design, trans-
parency, and responsible use of AI technologies.""" ,

"""Conclusions:
The findings of our study reveal that there exists a significant gap between the priorities
of students and those of current ranking institutions. More often than not, traditional
ranking metrics are an inversion of student priorities. It was clearly observed that univer-sities consistently maintain comprehensive data on metrics utilized by traditional ranking
institutions. The inverse is also true when it came to what students found to be impor-
tant. Based on this information one can assume that not only do institutions merely rank
and evaluate universities, they also fundamentally influence what universities prioritize
and measure.
It should not come as a surprise that ranking systems may currently be functioning as
a form of governance mechanism. As universities strive to climb or maintain their pres-
tigious rankings, universities are seemingly aligning themselves with ranking criteria at
the expense of factors more relevant to student values. This gap presents a strategic
opportunity for Chalmers and GU as they are able to capitalize on the disconnect be-
tween students and ranking institutions. Long-term success could possible rely more
heavily on how students perceive education quality than which ranking Chalmers or GU
hold. If Chalmers and GU prioritize an approach that reflect student prioritizes above
ranking metrics this can build a more authentic reputation. Satisfied student will act as
ambassadors for the institutions further strengthening reputation."""]


    return data



def prepare_embedding():
    load_dotenv(Path(".env.local"))
    openai.api_key = os.getenv('API_KEY')
    vector_data = [embed_text(text) for text in get_all_data()]
    with open('embedded_data.json','w') as file:
        json.dump(vector_data, file)
        print("Embedding done!")


prepare_embedding()