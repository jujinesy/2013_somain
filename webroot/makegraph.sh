#!/bin/bash
./manage.py graph_models document member project -o ../report/graph/Document_Member_Project.png
./manage.py graph_models document -o ../report/graph/Document.png
./manage.py graph_models lectureroom -o ../report/graph/Lectureroom.png
./manage.py graph_models mail -o ../report/graph/Mail.png
./manage.py graph_models manager -o ../report/graph/Manager.png
./manage.py graph_models member -o ../report/graph/SomaUser.png
./manage.py graph_models mobile -o ../report/graph/Mobile.png
./manage.py graph_models project -o ../report/graph/Project.png
./manage.py graph_models structure -o ../report/graph/Structure.png