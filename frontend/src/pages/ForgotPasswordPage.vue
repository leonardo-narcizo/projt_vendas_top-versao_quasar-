<template>
    <div>
        <h2>FORGET senha: {{ teste }}</h2>
    </div>
</template>

<script>
import { ref } from 'vue'

export default {
    setup () {
        const teste = ref('teste')

        return teste
    }
}
</script>
