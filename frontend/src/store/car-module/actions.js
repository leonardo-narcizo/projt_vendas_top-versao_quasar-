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
            commit('setUrlImage', data.url_imagem)
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