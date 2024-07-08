<template>
    <div class="q-pa-md">
      <div class="q-gutter-md">
        <q-carousel
          v-model="slide"
          transition-prev="jump-right"
          transition-next="jump-left"
          swipeable
          animated
          control-color="secondary"
          prev-icon="arrow_left"
          next-icon="arrow_right"
          padding
          arrows
          height="400px"
          class="bg-transparent text-white shadow-1 rounded-borders"
        >
          <q-carousel-slide name="vendas" class="column no-wrap flex-center">
            <div class="q-mt-md text-center">
              <h2>Gráfico de Vendas</h2>
              <img :src="graficoVendas" alt="Gráfico de Vendas" style="max-width: 100%;" />
            </div>
          </q-carousel-slide>
          <q-carousel-slide name="compras" class="column no-wrap flex-center">
            <div class="q-mt-md text-center">
              <h2>Gráfico de Compras</h2>
              <img :src="graficoCompras" alt="Gráfico de Compras" style="max-width: 100%;" />
            </div>
          </q-carousel-slide>
        </q-carousel>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    setup() {
      const slide = ref('vendas');
      const graficoVendas = ref(null);
      const graficoCompras = ref(null);
  
      // Carregar gráfico de vendas
      const carregarGraficoVendas = async () => {
        try {
          const token = sessionStorage.getItem('token');
          const response = await axios.post('/grafico_vendas', { username: 'seu_username', inicio: 'data_inicio', fim: 'data_fim' }, {
            headers: { Authorization: token }
          });
          graficoVendas.value = URL.createObjectURL(new Blob([response.data]));
        } catch (error) {
          console.error('Erro ao carregar gráfico de vendas:', error);
        }
      };
  
      // Carregar gráfico de compras
      const carregarGraficoCompras = async () => {
        try {
          const token = sessionStorage.getItem('token');
          const response = await axios.post('/grafico_compras', { username: 'seu_username', inicio: 'data_inicio', fim: 'data_fim' }, {
            headers: { Authorization: token }
          });
          graficoCompras.value = URL.createObjectURL(new Blob([response.data]));
        } catch (error) {
          console.error('Erro ao carregar gráfico de compras:', error);
        }
      };
  
      onMounted(async () => {
        await carregarGraficoVendas();
        await carregarGraficoCompras();
      });
  
      return {
        slide,
        graficoVendas,
        graficoCompras
      };
    },
  };
  </script>
  
  <style scoped>
  /* Estilos do seu componente aqui */
  .q-pa-md {
    padding: 1rem;
  }
  
  .q-gutter-md {
    margin-left: -1rem;
    margin-right: -1rem;
  }
  
  .text-center {
    text-align: center;
  }
  
  .q-mt-md {
    margin-top: 1rem;
  }
  </style>
  