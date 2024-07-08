export function setIsSent(state, result) {
    state.novaProposta.isSent = result
}

export function setSendProposalResult(state, result) {
    state.novaProposta.sendProposalResult = result
}

export function setProposalsOnList(state, result) {
    state.showProposals.proposalsList = result
}

export function setProposalsSearchResult(state, result) {
    state.showProposals.proposalsSearchResult = result
}

export function setFailedToFetchAPI(state, result) {
    state.showProposals.failedToFetchAPI = result
}

export function setIdOnCurrentProposal(state, id) {
    state.currentProposal.id_proposta = id
}

export function setProposalMessageResult(state, result) {
    state.currentProposal.proposalMessageResult = result
}

export function setConfirmResult(state, result) {
    state.currentProposal.confirmResult = result
}

export function clearCurrentProposal(state) {
    state.currentProposal.proposalMessageResult = ''
    state.currentProposal.confirmResult = false
}