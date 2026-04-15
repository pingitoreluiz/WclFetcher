DIFFICULTIES = {"Normal": 3, "Heroic": 4, "Mythic": 5}

WOW_CLASSES = {
    "Death Knight": ["Blood", "Frost", "Unholy"],
    "Demon Hunter": ["Devourer", "Havoc", "Vengeance"],
    "Druid": ["Balance", "Feral", "Guardian", "Restoration"],
    "Evoker": ["Augmentation", "Devastation", "Preservation"],
    "Hunter": ["Beast Mastery", "Marksmanship", "Survival"],
    "Mage": ["Arcane", "Fire", "Frost"],
    "Monk": ["Brewmaster", "Mistweaver", "Windwalker"],
    "Paladin": ["Holy", "Protection", "Retribution"],
    "Priest": ["Discipline", "Holy", "Shadow"],
    "Rogue": ["Assassination", "Outlaw", "Subtlety"],
    "Shaman": ["Elemental", "Enhancement", "Restoration"],
    "Warlock": ["Affliction", "Demonology", "Destruction"],
    "Warrior": ["Arms", "Fury", "Protection"]
}

CLASS_COLORS = {
    "Death Knight": "#C41F3B",
    "Demon Hunter": "#A330C9",
    "Druid": "#FF7C0A",
    "Evoker": "#33937F",
    "Hunter": "#AAD372",
    "Mage": "#3FC7EB",
    "Monk": "#00FF96",
    "Paladin": "#F48CBA",
    "Priest": "#FFFFFF",
    "Rogue": "#FFF468",
    "Shaman": "#0070DE",
    "Warlock": "#8788EE",
    "Warrior": "#C69B6D"
}

TRANSLATIONS = {
    "en": {
        "api_setup": "API Configuration",
        "client_id": "WCL Client ID",
        "client_secret": "WCL Client Secret",
        "char_setup": "Your Character",
        "connect_btn": "Connect and Fetch Raids",
        "raids_title": "Recent Raids / Encounters (Click on a boss)",
        "open_log": "🔗 Access Full Log",
        "auth_msg": "Authenticating and connecting to Warcraft Logs...\n",
        "cred_err": "Please provide Warcraft Logs credentials!",
        "search_msg": "Please wait... fetching rank #1 for {0} {1} on {2} ({3})...\n",
        "rank_err": "No rankings match the parameters on WCL (incorrect spelling or no public log available).",
        "talents_err": "Talent String not found directly via API for this log. Access the full log below.",
        "fetch_err": "Unfortunately, talents could not be retrieved:\n{0}",
        "player": "Player: ",
        "throughput": " with a throughput of ",
        "talent_header": "=== HOW TO GET THE TALENTS ===\n",
        "success_msg": "🔗 Direct Link Generated Successfully!\n\n1. Click the blue 'Access Full Log' button below.\n2. Warcraft Logs will open directly on this player's talents.\n3. Finally, just click the 'Copy Talent String' button on the WCL website!",
        "v2_macro_info": "\n\n=== MACRO COMMAND (V2 Experimental) ===\nCopy the command below and paste in WoW chat:",
        "v2_macro_err": "Failed to extract exact talent IDs from API."
    },
    "pt": {
        "api_setup": "Configuração da API",
        "client_id": "WCL Client ID",
        "client_secret": "WCL Client Secret",
        "char_setup": "Seu Personagem",
        "connect_btn": "Conectar e Buscar Raides",
        "raids_title": "Raides / Encontros Recentes (Clique em um chefão)",
        "open_log": "🔗 Acessar Log Completo",
        "auth_msg": "Autenticando e conectando com o Warcraft Logs...\n",
        "cred_err": "Por favor, forneça as credenciais do Warcraft Logs!",
        "search_msg": "Aguarde... pesquisando o rank #1 de {0} {1} para {2} ({3})...\n",
        "rank_err": "Nenhum ranking listado no WCL atingiu os parâmetros (Ortografia incorreta ou sem log público disponível).",
        "talents_err": "String de Talentos não encontrada diretamente via API para este log. Acesse a URL abaixo.",
        "fetch_err": "Infelizmente não foi possível obter os talentos:\n{0}",
        "player": "Jogador: ",
        "throughput": " com um throughput de ",
        "talent_header": "=== COMO PEGAR OS TALENTOS ===\n",
        "success_msg": "🔗 Link Direto Gerado com Sucesso!\n\n1. Clique no botão azul 'Acessar Log Completo' abaixo.\n2. O Warcraft Logs vai abrir diretamente nos talentos deste jogador.\n3. Basta clicar no botão 'Copy Talent String' no site da WCL!",
        "v2_macro_info": "\n\n=== COMANDO DE MACRO (V2 Experimental) ===\nCopie o comando abaixo e cole no chat do WoW:",
        "v2_macro_err": "Falha ao extrair IDs exatos de talentos via API."
    }
}
