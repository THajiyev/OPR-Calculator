import numpy as np
import requests
import yaml
from scipy.linalg import solve

event = yaml.load(open("keys.yaml"), Loader=yaml.FullLoader)['event']
auth = yaml.load(open("keys.yaml"), Loader=yaml.FullLoader)['auth']
print(event)
print(auth)
headers={'X-TBA-Auth-Key': auth}
teams_link =  "https://www.thebluealliance.com/api/v3/event/"+event+"/teams/simple"
matches_link = "https://www.thebluealliance.com/api/v3/event/"+event+"/matches/simple"

scores = []
matrix_a = []
teams = [team['key'] for team in requests.get(url=teams_link, headers=headers).json()]

def get_row(alliance_data):
    row = [0]*len(teams)
    for team in alliance_data["team_keys"]:
        row[teams.index(team)]=1
    return row

for match in requests.get(url=matches_link, headers=headers).json():
    if match['comp_level']=='qm':
        alliances_data = [match["alliances"]['red'],match["alliances"]['blue']]
        for alliance_data in alliances_data:
            scores.append(alliance_data["score"])
            matrix_a.append(get_row(alliance_data))

matrix_a = np.array(matrix_a) 
scores = np.array(scores)
oprs = solve(np.matmul(matrix_a.transpose(), matrix_a), np.matmul(matrix_a.transpose(), scores))
final_data = sorted(zip(teams, oprs.tolist()), key=lambda x:x[1], reverse=True)
for [team, opr] in final_data:
    print(team[3:]+": "+str(round(opr, 2)))
