export function setIsPosted(state, result) {
    state.novoCarro.isPosted = result
}

export function setPostResult(state, result) {
    state.novoCarro.postResult = result
}

export function setCarsOnList (state, cars) {
    state.listaCarros = cars
}

export function setSearchResult (state, result) {
    state.searchResult = result
}

export function setLastestSoldCars (state, cars) {
    state.lastestSoldCars.first = cars[0]
    state.lastestSoldCars.second = cars[1]
    state.lastestSoldCars.third = cars[2]
}

export function setDisponibleBrands (state, brands_list) {
    state.disponibleBrands = brands_list
}

export function setBrandId (state, brand_id) {
    state.brand_id = brand_id
}

export function setDisponibleModels (state, models_list) {
    state.disponibleModels = models_list
}

export function setDisponibleYears (state, years_list) {
    state.disponibleYears = years_list
}