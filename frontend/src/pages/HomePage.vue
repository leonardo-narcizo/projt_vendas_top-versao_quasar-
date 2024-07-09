<template>
  <div>
    <h4 class="homeTitle text-center q-mb-lg q-py-md bg-secondary">Confira as Últimas notícias</h4>

    <!-- Últimos Carros Vendidos -->
    <div class="section">
      <h5>Últimos Carros Vendidos</h5>
      <div class="car-list">
        <!-- Carro Vendido 1 -->
        <div class="car-item">
          <img :src="urlImage" alt="Fiat Uno" class="car-image">
          <div class="car-info">Fiat Uno</div>
        </div>
        <!-- Carro Vendido 2 -->
        <div class="car-item">
          <img src="https://3.bp.blogspot.com/-vopx9ywF2Qc/U4QmoCvkekI/AAAAAAABW_U/OhjB3glJfSk/s1600/Novo-Honda-Civic-2015+(1).jpg" alt="Honda Civic" class="car-image">
          <div class="car-info">Honda Civic</div>
        </div>
        <!-- Carro Vendido 3 -->
        <div class="car-item">
          <img src="https://th.bing.com/th/id/OIP.lHoc9Mh-pd7arpvhqG4ZnQAAAA?rs=1&pid=ImgDetMain" alt="Ford Fusion" class="car-image">
          <div class="car-info">Ford Fusion</div>
        </div>
      </div>
    </div>

    <!-- Últimos Carros Comprados -->
    <div class="section">
      <h5>Últimos Carros Colocados em Catálogo</h5>
      <div class="car-list">
        <!-- Placeholder para lista de carros comprados -->
        <div class="car-item">Carro Comprado 1</div>
        <div class="car-item">Carro Comprado 2</div>
        <div class="car-item">Carro Comprado 3</div>
      </div>
    </div>

    <!-- Carros em Destaque -->
    <div class="section">
      <h5>Carros em Destaque</h5>
      <div class="car-list">
        <!-- Placeholder para carros em destaque -->
        <div class="car-item">Carro Destaque 1</div>
        <div class="car-item">Carro Destaque 2</div>
        <div class="car-item">Carro Destaque 3</div>
      </div>
    </div>

    <!-- Insights de Mercado -->
    <div class="section">
      <h5>Insights de Mercado</h5>
      <div class="insights-list">
        <!-- Placeholder para insights de mercado -->
        <div class="insight-item">Insight 1</div>
        <div class="insight-item">Insight 2</div>
        <div class="insight-item">Insight 3</div>
      </div>
    </div>

    <!-- Notícias e Atualizações -->
    <div class="section">
      <h5>Notícias e Atualizações</h5>
      <div class="news-list">
        <!-- Placeholder para notícias e atualizações -->
        <div class="news-item">Notícia 1</div>
        <div class="news-item">Notícia 2</div>
        <div class="news-item">Notícia 3</div>
      </div>
    </div>

    <!-- Depoimentos de Usuários -->
    <div class="section">
      <h5>Depoimentos de Usuários</h5>
      <div class="testimonials-list">
        <!-- Placeholder para depoimentos de usuários -->
        <div class="testimonial-item">Depoimento 1</div>
        <div class="testimonial-item">Depoimento 2</div>
        <div class="testimonial-item">Depoimento 3</div>
      </div>
    </div>

    <!-- Estatísticas do Site -->
    <div class="section">
      <h5>Estatísticas do Site</h5>
      <div class="stats-list">
        <!-- Placeholder para estatísticas do site -->
        <div class="stat-item">Total de Carros Vendidos: 100</div>
        <div class="stat-item">Total de Propostas: 200</div>
        <div class="stat-item">Usuários Ativos: 300</div>
      </div>
    </div>

    <!-- Eventos ou Promoções -->
    <div class="section">
      <h5>Eventos ou Promoções</h5>
      <div class="events-list">
        <!-- Placeholder para eventos ou promoções -->
        <div class="event-item">Evento 1</div>
        <div class="event-item">Promoção 1</div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    const urlImage = computed(() => store.getters['car/getUrlImage'])
  
    return {
      urlImage
    };
  },
};
</script>

<style lang="scss" scoped>
.section {
  margin-bottom: 2rem;
  background-color: $primary;
  margin-left: 5%;
  margin-right: 5%;
  border-radius: 5px;
}

.car-list, .proposal-list, .insights-list, .news-list, .testimonials-list, .stats-list, .events-list {
  display: flex;
  flex-wrap: wrap;
}

.car-item, .proposal-item, .insight-item, .news-item, .testimonial-item, .stat-item, .event-item {
  background-color: $secondary;
  border: 1px solid black;
  border-radius: 5px;
  padding: 1rem;
  margin: 0.5rem;
  flex: 1 1 calc(33% - 1rem);
  box-sizing: border-box;
  text-align: center; /* Adiciona centralização ao conteúdo */
}

.car-image {
  width: 100%;
  height: auto;
  max-height: 270px; /* Define uma altura máxima para a imagem */
  object-fit: cover; /* Faz com que a imagem se ajuste dentro do card, mantendo a proporção */
  border-radius: 5px;
  margin-bottom: 0.5rem;
}

.text-center {
  text-align: center;
}

.q-mb-lg {
  margin-bottom: 2rem;
}

.homeTitle {
  margin-left: 5%;
  margin-right: 5%;
  padding-inline: -30%;
  border: 1px solid black;
  border-radius: 5px;
}
</style>
