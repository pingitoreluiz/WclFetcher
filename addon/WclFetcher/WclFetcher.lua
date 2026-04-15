SLASH_WCLTALENTS1 = "/wcltalents"

SlashCmdList["WCLTALENTS"] = function(msg)
    if not msg or msg == "" then
        print("|cFFFFFF00[WCL Fetcher]|r Uso: Copie o comando gerado pelo App e cole aqui.")
        return
    end

    local classStr, specStr, nodesStr = strsplit(" ", msg, 3)
    
    if not nodesStr then
        print("|cFFFF0000[WCL Fetcher]|r Formato inválido.")
        return
    end

    local configID = C_ClassTalents.GetActiveConfigID()
    if not configID then
        print("|cFFFF0000[WCL Fetcher]|r Erro: não foi possível obter a árvore de talentos ativa.")
        return
    end

    -- Split nodes
    local nodes = {strsplit(",", nodesStr)}
    local allocatedCount = 0
    
    for _, nodeData in ipairs(nodes) do
        -- nodeData = "nodeID:rank:traitID"
        local nodeIDStr, rankStr, traitIDStr = strsplit(":", nodeData)
        local nodeID = tonumber(nodeIDStr)
        local targetRank = tonumber(rankStr)
        local traitID = tonumber(traitIDStr)

        if nodeID and targetRank then
            local nodeInfo = C_Traits.GetNodeInfo(configID, nodeID)
            
            if nodeInfo and nodeInfo.entryIDs and #nodeInfo.entryIDs > 0 then
                local bestEntryID = nodeInfo.entryIDs[1]
                
                -- Se a node é uma escolha, a API as vezes tem múltiplos entries.
                -- Usamos traitID para tentar encontrar a correta se for possivel no futuro.
                -- Por agora, fallback para o ativo ou o primeiro (MVP).
                if nodeInfo.activeEntry and nodeInfo.activeEntry.entryID then
                    bestEntryID = nodeInfo.activeEntry.entryID
                end
                
                for r = 1, targetRank do
                    local success = C_Traits.SetNodeSelection(configID, nodeID, bestEntryID)
                    if success then
                        allocatedCount = allocatedCount + 1
                    end
                end
            end
        end
    end

    C_Traits.CommitConfig(configID)
    print("|cFF00FF00[WCL Fetcher]|r Árvore populada! Foram encontrados requisições de rank na string do site.")
    print("|cFFFFFF00Nota:|r Para Choice Nodes complexos, verifique sua aba de talentos. Limpe a aba antes de importar para melhores resultados!")
end

print("|cFF00FFFFWCL Fetcher Addon carregado.|r Digite /wcltalents para usar ou cole a string exportada do App Python.")
