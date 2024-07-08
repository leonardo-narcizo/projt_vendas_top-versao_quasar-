<template>
  <div class="container">
    <q-btn 
      class="toggle-right-drawer-btn" 
      dense flat round icon="filter_alt" 
      label="Filtros"
      color="secondary"
      @click="toggleRightDrawer" 
    />
    
    <q-drawer class="bg-secondary" v-model="rightDrawerOpen" side="right" :style="{ top: '56px' }">
      <q-toolbar class="drawer-toolbar text-center">
        <q-toolbar-title>Filtrar por:</q-toolbar-title>
      </q-toolbar>
      <q-list>
        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Marca</q-item-label>
          </q-item-section>
          <q-item-section>
            <q-toggle v-model="filters.marca" />
          </q-item-section>
        </q-item>
        <q-item v-show="filters.marca">
          <q-item-section>
            <q-input placeholder="Digite uma marca" v-model="filterInputs.marca" />
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Modelo</q-item-label>
          </q-item-section>
          <q-item-section>
            <q-toggle v-model="filters.modelo" />
          </q-item-section>
        </q-item>
        <q-item v-show="filters.modelo">
          <q-item-section>
            <q-input placeholder="Digite um modelo" v-model="filterInputs.modelo" />
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Ano</q-item-label>
          </q-item-section>
          <q-item-section>
            <q-toggle v-model="filters.ano" />
          </q-item-section>
        </q-item>
        <q-item v-show="filters.ano">
          <q-item-section>
            <q-input placeholder="Ano mínimo" v-model="filterInputs.ano.ano_min" />
            <q-input placeholder="Ano máximo" v-model="filterInputs.ano.ano_max" />
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Quilometragem</q-item-label>
          </q-item-section>
          <q-item-section>
            <q-toggle v-model="filters.quilometragem" />
          </q-item-section>
        </q-item>
        <q-item v-show="filters.quilometragem">
          <q-item-section>
            <q-input placeholder="Quilometragem mínima" v-model="filterInputs.quilometragem.quil_min" />
            <q-input placeholder="Quilometragem máxima" v-model="filterInputs.quilometragem.quil_max" />
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Preço</q-item-label>
          </q-item-section>
          <q-item-section>
            <q-toggle v-model="filters.preco" />
          </q-item-section>
        </q-item>
        <q-item v-show="filters.preco">
          <q-item-section>
            <q-input placeholder="Preço mínimo" v-model="filterInputs.preco.preco_min" />
            <q-input placeholder="Preço máximo" v-model="filterInputs.preco.preco_max" />
          </q-item-section>
        </q-item>

        <q-item>
          <q-item-section>
            <q-item-label>
              <q-btn class="btn-submit" @click="searchCar">Buscar</q-btn>
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>
    
    <!-- Conteúdo principal da página -->
    <q-card class="main-content q-mt-xl">
      <show-cars-component-vue  class="content" v-if="showCars" />
    </q-card>

    <status-on-footer
        :show-footer="showFooter"
        :status="footerStatus"
        :message="footerMessage"
        @update-show-footer="updateShowFooter"
      />
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import StatusOnFooter from 'src/components/StatusOnFooter.vue'
import ShowCarsComponentVue from '../components/ShowCarsComponent.vue'

export default {
  components: {
    StatusOnFooter,
    ShowCarsComponentVue
  },
  setup () {
    const rightDrawerOpen = ref(true)

    const updateShowFooter = (value) => {
      showFooter.value = value;
    }

    const showFooter = ref(false)
    const footerStatus = ref('')
    const footerMessage = ref('')
    const showCars = ref(false)
    const carros = computed(() => store.getters['car/getCars'])
    const errorMessage = computed(() => store.getters['car/getSearchResult'])
    
    const store = useStore()

    const filters = ref({
      marca: false,
      modelo: false,
      ano: false,
      quilometragem: false,
      preco: false
    })

    // Inputs dinâmicos
    const filterInputs = ref({
      marca: '',
      modelo: '',
      ano: {
        ano_min: '',
        ano_max: ''
      },
      quilometragem: {
        quil_min: '',
        quil_max: ''
      },
      preco: {
        preco_min: '',
        preco_max: ''
      }
    })

    const toggleRightDrawer = () => {
      rightDrawerOpen.value = !rightDrawerOpen.value
    }

    // Funcition to validate what filters are axtivated and not empty
    const getActiveFilters = () => {
      const activeFilters = {}

      if (filters.value.marca) {
        if (filterInputs.value.marca != '') {
          activeFilters.marca = filterInputs.value.marca;
        } else {
          showFooter.value = true;
          footerStatus.value = 'error';
          footerMessage.value = 'Digite uma marca!';
          return
        }
      }

      if (filters.value.modelo) {
        if (filterInputs.value.modelo != '') {
          activeFilters.modelo = filterInputs.value.modelo;
        } else {
          showFooter.value = true;
          footerStatus.value = 'error';
          footerMessage.value = 'Digite um modelo!';
          return
        }
      }

      if (filters.value.ano) {
        if (filterInputs.value.ano.ano_min != '' || filterInputs.value.ano.ano_max != '') {
          activeFilters.ano = {
            ano_minimo: filterInputs.value.ano.ano_min,
            ano_maximo: filterInputs.value.ano.ano_max
          };
        } else {
          showFooter.value = true;
          footerStatus.value = 'error';
          footerMessage.value= 'Digite um ano mínimo ou máximo!';
          return
        }
      }

      if (filters.value.quilometragem) {
        if (filterInputs.value.quilometragem.quil_min || filterInputs.value.quilometragem.quil_max) {
          activeFilters.quilometragem = {
            quilometragem_minima: filterInputs.value.quilometragem.quil_min,
            quilometragem_maxima: filterInputs.value.quilometragem.quil_max
          };
        } else {
          showFooter.value = true;
          footerStatus.value = 'error';
          footerMessage.value = 'Digite uma quilometragem mínima ou máxima!';
          return
        }
      }

      if (filters.value.preco) {
        if (filterInputs.value.preco.preco_min || filterInputs.value.preco.preco_max) {
          activeFilters.preco = {
            preco_minimo: filterInputs.value.preco.preco_min,
            preco_maximo: filterInputs.value.preco.preco_max
          };
        } else {
          showFooter.value = true;
          footerStatus.value = 'error';
          footerMessage.value = 'Digite um preço mínimo ou máximo!';
          return
        }
      }

      return activeFilters
    }

    // Function p/ mesclar os resultados de todas requests de filtro (função mais importante de merge)
    const combineResults = (results) => {
      if (results.length === 1) {
        return results[0]
      }
      return results.reduce((acc, current) => {
        return acc.filter(car => current.some(c => c.id === car.id))
      })
    }

    const searchCar = async () => {
      const activeFilters = getActiveFilters()

      const requests = []

      if (Object.keys(activeFilters).length === 0) {
        requests.push(store.dispatch('car/searchAllCars'))
      }

      if (activeFilters.marca) {
        requests.push(store.dispatch('car/searchByMarca', activeFilters.marca))
      }
      if (activeFilters.modelo) {
        requests.push(store.dispatch('car/searchByModelo', activeFilters.modelo))
      }
      if (activeFilters.ano) {
        requests.push(store.dispatch('car/searchByAno', activeFilters.ano))
      }
      if (activeFilters.quilometragem) {
        requests.push(store.dispatch('car/searchByQuilometragem', activeFilters.quilometragem))
      }
      if (activeFilters.preco) {
        requests.push(store.dispatch('car/searchByPreco', activeFilters.preco))
      }

      try {
        const results = await Promise.all(requests)
        var combinedResults = combineResults(results)
        store.commit('car/setCarsOnList', combinedResults)

        console.log('carros.value:', carros.value);
        console.log('Object.keys(activeFilters).length:', Object.keys(activeFilters).length);

        if (carros.value.length === 0) {
          if (Object.keys(activeFilters).length === 1) {
            showFooter.value = true
            footerStatus.value = 'error'
            footerMessage.value = errorMessage.value
          } else {
            showFooter.value = true
            footerStatus.value = 'error'
            footerMessage.value = 'Não há carros com os filtros especificados'
          }
        } else {
          showCars.value = true
        }
      } catch (error) {
        console.log('carros.value:', carros.value);
        console.log('result', combinedResults.value)
        console.log('Object.keys(activeFilters).length:', Object.keys(activeFilters).length);
        showFooter.value = true
        footerStatus.value = 'error'
        footerMessage.value = 'Erro durante a comunicação com o servidor'
      }
    }

    return {
      rightDrawerOpen,
      filters,
      filterInputs,
      searchCar,
      toggleRightDrawer,
      showFooter,
      footerStatus,
      footerMessage,
      updateShowFooter,
      getActiveFilters,
      showCars,
      carros,
      errorMessage
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  position: relative;
  padding: 20px;
  background-color: transparent;
}

.toggle-right-drawer-btn {
  position: absolute;
  top: 10px;
  right: 20px;
  z-index: 1;
}

.drawer-toolbar {
  background-color: $secondary;
  color: black;
  background-color: $primary;
}

.btn-submit {
  border: 2px solid black;
  border-radius: 5px;;
  display: inline-block;
  margin: 0
}
.main-content {
  background-color: transparent;
}
</style>
