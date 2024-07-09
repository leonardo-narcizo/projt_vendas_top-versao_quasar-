<template>
  <div class="q-pa-xl">
    <q-card>
      <q-card-section>
        <div class="text-h6 text-center">Cadastro de Novo Carro à Venda</div><br>
        <div class="text-subtitle2 q-mb-xs">Preencha o formulário abaixo com os dados do seu carro:</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit.prevent="handleSubmit" class="form" enctype="multipart/form-data">
          <q-input v-model="marca" label="Digite o fabricante" type="text" standard />
          <q-input v-model="modelo" label="Digite o modelo" type="text" standard />
          <q-input v-model="ano" label="Digite o ano de fabricação" type="number" standard />
          <q-input v-model="quilometragem" label="Digite a quilometragem" type="number" standard />
          <q-input v-model="preco" label="Digite o preço" type="number" standard />
          <q-file v-model="file" label="Anexar imagem do carro" accept=".jpg,.png,.jpeg" @change="handleFileChange" />
          <q-btn type="submit" label="Colocar carro à venda" color="secondary" class="btn q-py-sm" />
        </q-form>
      </q-card-section>

      <status-on-footer
        :show-footer="showFooter"
        :status="footerStatus"
        :message="footerMessage"
        @update-show-footer="updateShowFooter"
      />
    </q-card>
  </div>
</template>

<script>
import StatusOnFooter from 'src/components/StatusOnFooter.vue';
import { ref, computed } from 'vue';
import { useStore } from 'vuex';

export default {
  components: {
    StatusOnFooter,
  },
  setup() {
    const updateShowFooter = (value) => {
      showFooter.value = value;
    };

    const store = useStore();
    const showFooter = ref(false);
    const footerStatus = ref('');
    const footerMessage = ref('');

    const username = sessionStorage.getItem('username');
    const marca = ref('');
    const modelo = ref('');
    const ano = ref('');
    const quilometragem = ref('');
    const preco = ref('');
    const file = ref(null); // Para armazenar o arquivo selecionado

    const isPosted = computed(() => store.getters['car/getIsPosted']);
    const postResult = computed(() => store.getters['car/getPostResult']);

    const handleFileChange = (files) => {
      file.value = files[0];
    };

    const handleSubmit = async () => {
      // Validando os campos preenchidos
      if (!marca.value || !modelo.value || !ano.value || !quilometragem.value || !preco.value || !file.value) {
        showFooter.value = true;
        footerStatus.value = 'error';
        footerMessage.value = 'Preencha todos os campos antes de cadastrar';
        return;
      }

      // Criando um novo FormData
      const formData = new FormData();
      formData.append('marca', marca.value);
      formData.append('modelo', modelo.value);
      formData.append('ano', ano.value);
      formData.append('quilometragem', quilometragem.value);
      formData.append('preco', preco.value);
      formData.append('username', username)
      formData.append('car_image', file.value); // Adicionando o arquivo de imagem

      // Envie para o backend usando FormData
      await store.dispatch('car/postCar', formData);

      if (isPosted.value) {
        showFooter.value = true;
        footerStatus.value = 'confirmed';
        footerMessage.value = postResult.value;
      } else {
        showFooter.value = true;
        footerStatus.value = 'error';
        footerMessage.value = postResult.value;
      }
    };

    return {
      marca,
      modelo,
      ano,
      quilometragem,
      preco,
      file,
      username,
      handleSubmit,
      footerStatus,
      footerMessage,
      showFooter,
      isPosted,
      postResult,
      updateShowFooter,
      handleFileChange
    };
  }
};
</script>

<style scoped>
.q-card {
  max-width: 600px; /* Definindo a largura máxima do q-card */
  margin: 0 auto; /* Centralizando o q-card */
}

.form {
  width: 100%; /* Garantindo que o formulário ocupe toda a largura do q-card */
  margin-top: -30px;
}

.btn {
  display: block;
  margin: auto;
  margin-top: 15px;
}
</style>
