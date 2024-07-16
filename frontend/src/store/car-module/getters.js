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

export function getLastestSoldCars (state) {
    return state.lastestSoldCars
}

// Getters da listagem de propriedades para cadastro de novo carro
export function getDisponibleBrands (state) {
    return state.disponibleBrands
}

export function getBrandId (state) {
    return state.brandId
}

export function getDisponibleModels (state) {
    return state.disponibleModels
}

export function getDisponibleYears (state) {
    return state.disponibleYears
}

