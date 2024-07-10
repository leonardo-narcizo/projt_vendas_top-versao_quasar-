<template>
  <div id="carro-container">
    <div v-for="carro in carros" :key="carro.id" class="carro">
      <div class="carro-info">
        <div class="carro-texto">
          <div>
            <span><strong>Marca:</strong></span> {{ carro.marca }}
          </div>
          <div>
            <span><strong>Modelo:</strong></span> {{ carro.modelo }}
          </div>
          <div>
            <span><strong>Ano:</strong></span> {{ carro.ano }}
          </div>
          <div>
            <span><strong>Quilometragem:</strong></span> {{ carro.quilometragem }}
          </div>
          <div>
            <span><strong>Preço:</strong></span> {{ carro.preco }}
          </div>
          <div>
            <span><strong>Proprietário:</strong></span> {{ carro.proprietario }}
          </div>
        </div>
        <div class="carro-imagem">
          <img v-if="carro.car_image != null" :src="carro.car_image" alt="sem imagem" class="car-image" />
          <div v-else class="image-placeholder">
            <span>Este carro não possui imagem</span>
        </div>
          <div class="text-right q-pt-sm">
            <q-btn color="secondary" text-color="black" @click="showMakeProposal(carro)">
              Fazer Proposta
            </q-btn>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialog para fazer proposta -->
    <MakeProposal
      v-model="isDialogOpen"
      @proposalSent="handleTrySendProposal"
      :carDescription="currentCar"
    />

    <!-- Componente do footer para dar feedback sobre a proposta -->
    <StatusOnFooter
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
    max-width: 800px;
    margin: 0 auto;
    background-color: transparent;
  }
  
  .carro {
    margin-top: 25px;
    border: 5px solid black;
    border-radius: 5px;
    padding: 10px;
    background-color: white;
  }
  
  .carro-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .carro-texto {
    width: 50%;
  }
  
  .carro-imagem {
    width: 40%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .car-image {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 5px;
    margin-bottom: 0.5rem;
  }

  .image-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background-color: #f0f0f0; /* Cor de fundo para a moldura */
    color: #666;
    font-size: 18px;
}
  </style>

  