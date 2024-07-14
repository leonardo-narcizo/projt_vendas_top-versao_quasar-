<template>
    <q-dialog v-model="isOpen" content-class="custom-dialog">
      <q-card class="main-card bg-secondary">
        <q-card-section>
          <div class="header text-h6 text-center q-mb-md q-mx-xl">Fazer Proposta</div>
          <q-list class="desc-list q-mx-xl">
            <q-item class="text-subtitle1">Descrição do carro:</q-item>
            <q-item><strong>Marca</strong>: {{ carDescription.marca }}</q-item>
            <q-item><strong>Modelo</strong>: {{ carDescription.modelo }}</q-item>
            <q-item><strong>Ano</strong>: {{ carDescription.ano }}</q-item>
            <q-item><strong>Quilometragem</strong>: {{ carDescription.quilometragem }}</q-item>
            <q-item><strong>Preço</strong>: {{ carDescription.preco }}</q-item>
            <q-item><strong>Proprietário</strong>: {{ carDescription.proprietario }}</q-item>
          </q-list>
        </q-card-section>
  
        <q-card-section>
          <!-- Conteúdo do formulário de proposta -->
          <q-input v-model="descricao" placeholder="Digite uma descrição da proposta" />
          <q-input type="number" v-model="proposalPrice" placeholder="Digite o preço inicial de negociação" no-stepper />
        </q-card-section>
  
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="negative" @click="closeDialog" />
          <div class="text-right">
            <q-btn flat label="Enviar" color="positive" class="send-btn" @click="sendProposal" />
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </template>
  
  <script>
  import { ref, watch, computed } from 'vue';
  import { useStore } from 'vuex';

  
  export default {
    props: {
      modelValue: {
        type: Boolean,
        required: true
      },
      carDescription: {
        type: Object
      }
    },
    emits: ['update:modelValue', 'proposalSent'],
    setup(props, { emit }) {
      const store = useStore()
      const isOpen = ref(props.modelValue)
      const descricao = ref('')
      const proposalPrice = ref('')

      watch(() => props.modelValue, (newVal) => {
        isOpen.value = newVal;
        if (newVal == false) {
            sessionStorage.removeItem('carro')
        }
      });
  
      watch(isOpen, (newVal) => {
        emit('update:modelValue', newVal);
      });
  
      const closeDialog = () => {
        isOpen.value = false;
      };

      const storedUsername = sessionStorage.getItem('username')
      const username = ref(storedUsername)

      const sendProposal = async () => {
        const storedCar = sessionStorage.getItem('carro')
        const convertedCar = JSON.parse(storedCar) // Agora isso é um objeto javascript, iremos mandar p actions, as propriedades dele
        
        console.log('username é:', storedUsername)
        console.log('proprietario é: ', convertedCar.proprietario)

        // Validando se o proprietário é o próprio usuario logado
        if (storedUsername == props.carDescription.proprietario) {
          console.log('erro pois ja é o dono')
          closeDialog()
          store.commit('proposal/setIsSent', false)
          store.commit('proposal/setSendProposalResult', 'Você já é o proprietário deste carro! Não é possivel compra-lo.')
          emit('proposalSent')
          return
        }

        await store.dispatch('proposal/sendProposal', {
          id_carro: convertedCar.id,
          nome_proprietario: convertedCar.proprietario,
          nome_comprador: username.value,
          descricao: descricao.value,
          preco_proposto: proposalPrice.value
        })


        isOpen.value = false
        emit('proposalSent')
      };
  
      return {
        isOpen,
        descricao,
        proposalPrice,
        username,
        closeDialog,
        sendProposal
      };
    }
  };
  </script>
  
<style lang="scss">
.q-dialog.custom-dialo {
    width: 500px;
}
.desc-list {
    border: 2px solid black;
    border-radius: 5px;
}
 </style>