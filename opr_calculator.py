import numpy as np
import requests
from scipy.linalg import solve

class OPR_Calculator:
    
    def __init__(self, auth):
        self.headers = {'X-TBA-Auth-Key': auth}
    
    def get_row(self, alliance_data, teams):
        row = [0]*len(teams)
        for team in alliance_data["team_keys"]:
            row[teams.index(team)]=1
        return row

    def get_oprs(self, event):
        teams_link =  "https://www.thebluealliance.com/api/v3/event/"+event+"/teams/simple"
        matches_link = "https://www.thebluealliance.com/api/v3/event/"+event+"/matches/simple"
        scores = []
        matrix_a = []
        teams = [team['key'] for team in requests.get(url=teams_link, headers=self.headers).json()]
        for match in requests.get(url=matches_link, headers=self.headers).json():
            if match['comp_level']=='qm':
                alliances_data = [match["alliances"]['red'],match["alliances"]['blue']]
                for alliance_data in alliances_data:
                    if alliance_data["score"]==-1:
                        break
                    scores.append(alliance_data["score"])
                    matrix_a.append(self.get_row(alliance_data, teams))
        matrix_a = np.array(matrix_a) 
        scores = np.array(scores)
        oprs = solve(np.matmul(matrix_a.transpose(), matrix_a), np.matmul(matrix_a.transpose(), scores))
        final_data = sorted(zip(teams, oprs.tolist()), key=lambda x:x[1], reverse=True)
        return final_data
    
    def print_oprs(self, event):
        final_data = self.get_oprs(event)
        for [team, opr] in final_data:
            print(team[3:]+": "+str(round(opr, 2)))
