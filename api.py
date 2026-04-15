import requests

class APIClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def authenticate(self):
        url = "https://www.warcraftlogs.com/oauth/token"
        auth = (self.client_id, self.client_secret)
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        self.token = response.json()['access_token']

    def query_graphql(self, query, variables=None):
        if not self.token:
            self.authenticate()
        url = "https://www.warcraftlogs.com/api/v2/client"
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.post(url, json={'query': query, 'variables': variables or {}}, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_latest_zones(self):
        query = """
        query {
            worldData {
                expansions {
                    id
                    zones {
                        id
                        name
                        encounters {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        data = self.query_graphql(query)
        expansions = data.get('data', {}).get('worldData', {}).get('expansions', [])
        expansions.sort(key=lambda x: x['id'], reverse=True)
        
        valid_zones = []
        for exp in expansions:
            zones = exp.get('zones', [])
            zones.sort(key=lambda x: x['id'], reverse=True)
            
            for z in zones:
                if z.get('encounters'):
                    name = z['name'].lower()
                    invalid_words = ["mythic+", "dungeon", "remix", "events", "challenge", "brawl", "test", "complete raids", "beta"]
                    if not any(word in name for word in invalid_words):
                        valid_zones.append(z)
                        
            if valid_zones:
                break
                
        return valid_zones[:5]

    def fetch_top_talents(self, encounter_id, class_name, spec_name, difficulty):
        api_class = class_name.replace(" ", "")
        api_spec = spec_name.replace(" ", "")
        
        query = """
        query($encounterID: Int!, $className: String!, $specName: String!, $difficulty: Int!) {
            worldData {
                encounter(id: $encounterID) {
                    characterRankings(className: $className, specName: $specName, difficulty: $difficulty)
                }
            }
        }
        """
        variables = {
            "encounterID": int(encounter_id),
            "className": api_class,
            "specName": api_spec,
            "difficulty": int(difficulty)
        }
        
        data = self.query_graphql(query, variables)
        if 'errors' in data:
            return None, f"Erro da API WCL: {data['errors'][0].get('message', str(data['errors']))}"
            
        encounter_data = data.get('data', {}).get('worldData', {}).get('encounter')
        if not encounter_data:
            return None, "Encontro não encontrado ou inválido no WCL."
            
        rankings = encounter_data.get('characterRankings', {})
        if not rankings:
            return None, "A API não retornou dados de rankings."
        
        rankings_list = rankings.get('rankings', [])
        if not rankings_list:
            return None, "A lista de rankings está vazia para esta dificuldade/classe."
            
        top_player = rankings_list[0]
        return top_player, None

    def fetch_actor_id(self, report_code, player_name):
        query = """
        query($code: String!) {
            reportData { 
                report(code: $code) {
                    masterData {
                        actors(type: "Player") {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        variables = {"code": report_code}
        
        data = self.query_graphql(query, variables)
        if 'errors' in data:
            return None, f"Erro na API ao buscar masterData: {data['errors'][0].get('message', '')}"
            
        report = data.get('data', {}).get('reportData', {}).get('report')
        if not report:
            return None, "Nenhum relatório encontrado."
            
        actors = report.get('masterData', {}).get('actors', [])
        # Find actor id
        actor = next((a for a in actors if a.get('name') == player_name), None)
        if not actor:
            return None, f"Jogador {player_name} não encontrado nos dados do log."
            
        return actor.get('id'), None
