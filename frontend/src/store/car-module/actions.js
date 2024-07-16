export async function postCar ({ commit }, formData) {
    let postResult = ''

    try {
        const response = await fetch('http://localhost:5000/criarCarro', {
            method: 'POST',
            body: formData
        })

        const data = await response.json()
        postResult = data.message

        if (postResult === 'Carro cadastrado para venda!') {
            commit('setIsPosted', true)
        }
    }
    catch(err) {
        console.error('[erro]: ', err)
        postResult = 'Erro ao enviar os dados ao servidor.'
    }
    finally {
        commit('setPostResult', postResult)
        console.log('msg do servidor: ', postResult)
    }
}


async function fetchData({ commit }, url, body) {
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await response.json();
    if (data.lista_carros.length === 0) {
        commit('setSearchResult', data.message); // No caso da API retornar um array vazio, indica q a chave 'message', conterá um erro
        commit('setCarsOnList', []);
        return data.lista_carros || [];
    } else {
        commit('setCarsOnList', data.lista_carros);
        return data.lista_carros;
    }
}

export async function searchAllCars({ commit }) {
    const response = await fetch('http://localhost:5000/carros');
    const data = await response.json();
    return data.lista_carros || [];
}

export async function searchByMarca({ commit }, marca) {
    return await fetchData({ commit }, 'http://localhost:5000/marca', { marca });
}

export async function searchByModelo({ commit }, modelo) {
    return await fetchData({ commit }, 'http://localhost:5000/modelo', { modelo });
}

export async function searchByAno({ commit }, { ano_minimo, ano_maximo }) {
    return await fetchData({ commit }, 'http://localhost:5000/ano', { ano_minimo, ano_maximo });
}

export async function searchByQuilometragem({ commit }, { quilometragem_minima, quilometragem_maxima }) {
    return await fetchData({ commit }, 'http://localhost:5000/quilometragem', { quilometragem_minima, quilometragem_maxima });
}

export async function searchByPreco({ commit }, { preco_minimo, preco_maximo }) {
    return await fetchData({ commit }, 'http://localhost:5000/preco', { preco_minimo, preco_maximo });
}


export async function searchLastestSoldCars( { commit } ) {
    const token = sessionStorage.getItem('token')

    try {
        const response = await fetch('http://localhost:5000/lastestSoldCars', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        
        const data = await response.json()

        if (response.ok) {
            commit('setLastestSoldCars', data.lastest_sold_cars)
        }
        else {
            commit('setSearchResult', data.message)
        }
    }
    catch (err) {
        console.error('[erro]: ', err)
    }
}


export async function searchDisponibleBrands( { commit } ) {
    try {
        const response = await fetch('http://localhost:5000/searchFipeBrands')

        const data = await response.json()

        if (response.ok) {
            commit('setDisponibleBrands', data.brands_list)
        }
        else {
            console.error('erro ao buscar marcas: ', data.message)
        }
    }
    catch (err) {
        console.error('erro ao buscar marcas; ', err)
    }
}


export async function searchDisponibleModels( { commit }, brand_id ) {
    try {
        const response = await fetch(`http://localhost:5000/searchFipeModels/${brand_id}`)

        const data = await response.json()

        if (response.ok) {
            commit('setDisponibleModels', data.models_list)
        }
        else {
            console.error('erro ao buscar modelos: ', data.message)
        }
    }
    catch (err) {
        console.error('erro ao buscar modelos; ', err)
    }
}


/* Amanhã por ultimo, configurar a rota de buscar as opcoes de ano de acordo com o modelo q é selecionado la no input,
e depois disso fazer a logica do envio da marca, modelo e ano, para a rota q buscará o preço médio para a descrição dada,
sobre um carro específico: primeiro iremos validar se todos inputs(c excessao do 'preco'), estão preenchidos
*/