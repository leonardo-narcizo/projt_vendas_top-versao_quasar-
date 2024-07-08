<template>
    <q-dialog :model-value="dialogVisible" @update:model-value="updateDialogVisible" content-class="custom-dialog">
      <q-card class="bg-secondary">
        <q-card-section class="">
          <div class="text-h6 text-center q-mb-md">Detalhes da Proposta</div>
          <div class="list q-mt-sm q-pa-xs q-mb-md">
            <p><strong>Marca:</strong> {{ proposal.marca }}</p>
            <p><strong>Modelo:</strong> {{ proposal.modelo }}</p>
            <p><strong>Enviado para:</strong> {{ proposal.proprietario_username }}</p>
            <p><strong>Data da Proposta:</strong> {{ proposal.data_proposta }}</p>
            <p><strong>Descrição da proposta:</strong> {{ proposal.descricao }}</p>
            <p><strong>Preço Proposto:</strong> {{ proposal.preco_proposto }}</p>
            <p v-if="currentFilter == 'encerrada'"><strong>Conclusão da proposta:</strong> {{ proposal.conclusao }}</p>
          </div>
        </q-card-section>
  
        <q-separator />

        <q-card-actions align="center">
            <q-btn label="Editar" color="primary" @click="editProposal" />
            <q-btn label="Cancelar proposta" color="negative" @click="cancelProposal" />
        </q-card-actions>
        </q-card>
    </q-dialog>
  </template>
  
  <script>
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
      editProposal() {
      this.$emit('edit')
    },
    cancelProposal() {
      this.$emit('cancel')
    }
    }
  };
  </script>
  
  <style lang="scss" scoped>
  .list {
    border: 2px solid black;
    border-radius: 5px;
  }
  </style>
  