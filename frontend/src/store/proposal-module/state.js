export default function () {
    return {
        novaProposta: {
            carroId: null,
            nomeComprador: null,
            descricao: '',
            precoProposto: null,
            sendProposalResult: '',
            isSent: false
        },
        showProposals: {
            proposalsList: [],
            proposalsSearchResult: '',
            failedToFetchAPI: false
        },
        currentProposal: {
            proposalMessageResult: '',
            confirmResult: false,
        }
    }
}
