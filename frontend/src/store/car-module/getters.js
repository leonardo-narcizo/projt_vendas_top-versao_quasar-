export function getIsPosted(state) {
    return state.novoCarro.isPosted
}

export function getPostResult(state) {
    return state.novoCarro.postResult
}

export function getCars(state) {
    return state.listaCarros
}

// Getter q irá trabalhar o funcionamento do footer dinâmico
export function getSearchResult(state) {
    return state.searchResult
}
