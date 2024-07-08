export async function sendProposal({ commit }, { id_carro, nome_proprietario, nome_comprador, descricao, preco_proposto }) {
    let sendProposalResult = ''

    try {
        const response = await fetch('http://localhost:5000/sendProposal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_carro,
                nome_proprietario,
                nome_comprador,
                descricao,
                preco_proposto
            })
        })

        const data = await response.json()
        sendProposalResult = data.message

        if (sendProposalResult === 'Proposta enviada com sucesso!') {
            commit('setIsSent', true)
        }
    }
    catch(err) {
        console.error('[erro]: ', err)
        sendProposalResult = 'Erro ao enviar os dados ao servidor'
    }
    finally {
        commit('setSendProposalResult', sendProposalResult)
    }
}


export async function searchProposals({ commit }, { tab, filter, username }) {
    let url = ''

    if (tab === 'received') {
        url = 'http://localhost:5000/showReceivedProposals'
    }
    else if (tab === 'sent') {
        url = 'http://localhost:5000/showSentProposals'
    }
    else {
        url = 'http://localhost:5000/showAllProposals'
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, situacao: filter })
        })

        const data = await response.json()

        if (data.lista_propostas.length === 0) {
            commit('setProposalsSearchResult', data.message)
            commit('setProposalsOnList', [])
            return data.lista_propostas || []
        }
        else {
            commit('setProposalsOnList', data.lista_propostas)
            return data.lista_propostas
        }
    }
    catch (err) {
        console.error('Erro ao buscar propostas', err)
        commit('setFailedToFetchAPI', true)
        commit('setProposalsSearchResult', 'Falha na comunicação com o servidor!')
        commit('setProposalsOnList', [])
    }
}

export async function rejectProposal({ commit }, { id_proposta }) {
    let proposalMessageResult = ''

    try {
        const response = await fetch('http://localhost:5000/rejectProposal', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id_proposta })
        })

        const data =  await response.json()
        proposalMessageResult = data.message

        if (data.message === 'Proposta recusada com sucesso!') {
            commit('setConfirmResult', true)
            commit('setProposalMessageResult', proposalMessageResult)
        }
        else {
            commit('setProposalMessageResult', proposalMessageResult)
        }
    }
    catch (err) {
        console.error('erro ao recusar proposta: ', err)
        commit('setProposalMessageResult', 'Falha na comunicação com o servidor!')
    }
}


export async function cancelProposal({ commit }, { id_proposta }) {
    let proposalMessageResult = ''

    try {
        const response = await fetch(`http://localhost:5000/cancelProposal/${id_proposta}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        const data =  await response.json()
        proposalMessageResult = data.message

        if (data.message === 'Proposta cancelada com sucesso!') {
            commit('setConfirmResult', true)
            commit('setProposalMessageResult', proposalMessageResult)
        }
        else {
            commit('setProposalMessageResult', proposalMessageResult)
        }
    }
    catch (err) {
        console.error('erro ao cancelar proposta: ', err)
        commit('setProposalMessageResult', 'Falha na comunicação com o servidor!')
    }
}


export async function negotiateProposal({ commit }, { id_proposta }) {
    let proposalMessageResult = ''

    try {
        const response = await fetch('http://localhost:5000/negotiateProposal', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id_proposta })
        })

        const data =  await response.json()
        proposalMessageResult = data.message

        if (data.message === 'Proposta colocada em negociação!') {
            commit('setConfirmResult', true)
            commit('setProposalMessageResult', proposalMessageResult)
        }
        else {
            commit('setProposalMessageResult', proposalMessageResult)
        }
    }
    catch (err) {
        console.error('erro ao colocar proposta em negociação: ', err)
        commit('setProposalMessageResult', 'Falha na comunicação com o servidor!')
    }
}


export async function acceptProposal({ commit }, { id_proposta, id_carro, comprador_username }) {
    let proposalMessageResult = ''

    try {
        const response = await fetch('http://localhost:5000/acceptProposal', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id_proposta })
        })

        const data =  await response.json()
        proposalMessageResult = data.message

        if (data.message === 'Proposta aceita com sucesso!') {
            try {
                const saleResponse = await fetch('http://localhost:5000/sellCar', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ id_carro, comprador_username})
                })

                const saleData = await saleResponse.json()
                proposalMessageResult = saleData.message

                if (saleData.message === 'carro vendido com sucesso!') {
                    commit('setConfirmResult', true)
                    commit('setProposalMessageResult', proposalMessageResult)
                }
                else {

                }
            }
            catch (err) {
                console.error('erro ao vender carro: ', err)
                commit('setProposalMessageResult', 'Falha na comunicação com o servidor!')
            }
        }
        else {
            commit('setProposalMessageResult', proposalMessageResult)
        }
    }
    catch (err) {
        console.error('erro ao aceitar proposta: ', err)
        commit('setProposalMessageResult', 'Falha na comunicação com o servidor!')
    }
}
