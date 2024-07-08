<template>
    <div id="carro-container">
      <div v-for="carro in carros" :key="carro.id" class="carro">
        <div class="carro-texto text-center text-subtitle2">
          | Marca: {{ carro.marca }} | Modelo: {{ carro.modelo }} | Ano: {{ carro.ano }} | Quilometragem: {{ carro.quilometragem }} | Preço: {{ carro.preco }} | Proprietário: {{ carro.proprietario }}
        </div>
        <div class="text-center q-pt-sm">
          <q-btn color="secondary" text-color="black" @click="showMakeProposal(carro)">Fazer Proposta</q-btn>
        </div>
      </div>

      <!-- Dialog para fazer proposta -->
      <MakeProposal 
        v-model="isDialogOpen"
        @proposalSent="handleTrySendProposal"
        :carDescription="currentCar"
      />

      <!--Componente do footer p dar o feedback sobre a proposta-->
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
  import MakeProposal from 'src/components/dialogs/MakeProposal.vue'
  import StatusOnFooter from 'src/components/StatusOnFooter.vue'
  
  export default {
    components: {
      MakeProposal,
      StatusOnFooter
    },
    setup() {
      const store = useStore()
      const carros = computed(() => store.getters['car/getCars'])
      const isDialogOpen = ref(false)
      const currentCar = ref(null)

      const updateShowFooter = (value) => {
        showFooter.value = value;
      }



      const showMakeProposal = (carro) => {
        isDialogOpen.value = true
        console.log(carro)
        currentCar.value = {
          id: carro.id,
          marca: carro.marca,
          modelo: carro.modelo,
          ano: carro.ano,
          quilometragem: carro.quilometragem,
          preco: carro.preco,
          proprietario: carro.proprietario
        }
        sessionStorage.setItem('carro', JSON.stringify(currentCar.value))
        const storedCar = sessionStorage.getItem('carro')
        const convertedCar = JSON.parse(storedCar)
        currentCar.value = convertedCar
        return currentCar.value
      }

      const showFooter = ref(false)
      const footerStatus = ref('')
      const footerMessage = ref('')

      const isSent = computed(() => store.getters['proposal/getIsSent'])
      const sendProposalResult = computed(() => store.getters['proposal/getSendProposalResult'])

      const handleTrySendProposal = () => {
        
        
        if (isSent.value == true) {
          showFooter.value = true
          footerStatus.value = 'confirmed'
          footerMessage.value = sendProposalResult.value
          console.log('Proposta Enviada')
        } 
        else {
          showFooter.value = true
          footerStatus.value = 'error'
          footerMessage.value = sendProposalResult.value
          console.log('Proposta falhou')
        }
      }
    
      return {
        carros,
        isDialogOpen,
        isSent,
        sendProposalResult,
        showFooter,
        footerStatus,
        footerMessage,
        showMakeProposal,
        handleTrySendProposal,
        updateShowFooter,
        currentCar
      }
    }
  }
  </script>
  
  <style lang="scss" scoped>
  #carro-container {
    max-width: 800px; /* Aumentando a largura */
    margin: 0 auto; /* Centraliza horizontalmente */
    text-align: left; /* Alinha o texto à esquerda */
    background-color: transparent;
  }
  
  .carro {
    
    margin-top: 25px;
    border: 5px solid black;
    border-radius: 5px;
    padding: 10px;
    position: relative; /* Torna a posição relativa para alinhar o botão */
    width: 100%; /* Define a largura para ocupar todo o espaço disponível */
    background-color: white;
  }
  </style>
  