export function getIsSent(state) {
    return state.novaProposta.isSent
}

export function getSendProposalResult(state) {
    return state.novaProposta.sendProposalResult
}

export function getProposalsList(state) {
    return state.showProposals.proposalsList
}

export function getProposalsSearchResult(state) {
    return state.showProposals.proposalsSearchResult
}

export function getProposalMessageResult(state) {
    return state.currentProposal.proposalMessageResult
}

export function getConfirmResult(state) {
    return state.currentProposal.confirmResult
}