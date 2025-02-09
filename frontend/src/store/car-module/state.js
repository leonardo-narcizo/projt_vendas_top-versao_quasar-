export default function () {
    return {
      novoCarro: {
        marca: '',
        modelo: '',
        ano: '',
        quilometragem: '',
        preco: '',
        proprietario: '',
        isPosted: false,
        postResult: ''
      },
      listaCarros: [], // Recebe um array para armazenar os carros recebidos da API
      searchResult: '',
      lastestSoldCars: {
        first: null,
        second: null,
        third: null
      },
      lastestCreatedCars: {
        first: null,
        second: null,
        third: null
      },
      disponibleBrands: [],
      disponibleModels: [],
      disponibleYears: []
    }
  }
  