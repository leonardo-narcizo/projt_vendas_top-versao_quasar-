<template>
  <q-dialog :model-value="dialogVisible" @update:model-value="updateDialogVisible" content-class="custom-dialog">
    <q-card class="bg-secondary">
      <q-card-section class="">
        <div class="text-h6 text-center q-mb-md">Detalhes da Proposta</div>
        <div class="list q-mt-sm q-pa-xs q-mb-md">
          <p><strong>Marca:</strong> {{ proposal.marca }}</p>
          <p><strong>Modelo:</strong> {{ proposal.modelo }}</p>
          <p><strong>Enviado por:</strong> {{ proposal.comprador_username }}</p>
          <p><strong>Data da Proposta:</strong> {{ proposal.data_proposta }}</p>
          <p><strong>Descrição da proposta:</strong> {{ proposal.descricao }}</p>
          <p><strong>Preço Proposto:</strong> {{ proposal.preco_proposto }}</p>
          <p v-if="currentFilter == 'encerrada'"><strong>Conclusão da proposta:</strong> {{ proposal.conclusao }}</p>
        </div>
      </q-card-section>

      <q-separator />

      <q-card-actions v-if="(currentFilter == 'nao_vista' && !soldCar) || (currentFilter == 'em_negociacao' && !soldCar)" align="center">
        <q-btn label="Recusar" color="negative" @click="rejectProposal" />
        <q-btn v-if="currentFilter == 'nao_vista'" label="Negociar" color="warning" @click="negotiateProposal" />
        <q-btn label="Aceitar" color="positive" @click="acceptProposal" />
      </q-card-actions>
      <div v-else>
        <div v-if="soldCar" class="text-center q-mb-lg text-subtitle1">Carro já Vendido</div>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, watch } from 'vue';
import { useStore } from 'vuex';

export default {
  props: {
    proposal: {
      type: Object,
      required: true
    },
    dialogVisible: {
      type: Boolean,
      required: true
    },
    currentFilter: {
      type: String,
      required: true
    }
  },
  methods: {
    updateDialogVisible(value) {
      this.$emit('update:modelValue', value);
    },
    acceptProposal() {
      this.$emit('accept');
    },
    negotiateProposal() {
      this.$emit('negotiate');
    },
    rejectProposal() {
      this.$emit('reject');
    }
  },
  setup(props) {
    const soldCar = ref(false);

    const checkCarStatus = (selectedProposal) => {
      if (selectedProposal.id_proprietario === selectedProposal.id_antigo_dono) {
        soldCar.value = true;
        console.log('Carro já vendido! Impossível tomar decisão.');
      } else if (selectedProposal.id_antigo_dono === null) {
        soldCar.value = false;
        console.log('Pode acionar sobre a proposta!');
      }
    };

    // Watchers para reavaliar o estado do carro sempre que a proposta mudar
    watch(() => props.proposal, (newProposalSelected) => {
      if (newProposalSelected) {
        checkCarStatus(newProposalSelected)
      }
    });

    return {
      soldCar
    };
  }
}
</script>

<style lang="scss" scoped>
.list {
  border: 2px solid black;
  border-radius: 5px;
}
</style>
