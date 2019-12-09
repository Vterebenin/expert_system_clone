<template lang="pug">
  v-container
    v-row
      v-col.text-center(cols="12")
        | Expert System Clone
    v-row
      v-col(cols="6")
        v-card(max-height="200" )
          v-card-title Результат
          v-card-text {{ output.join("\r\n") }}
      v-col(cols="6")
        v-card(max-height="200" )
          v-card-title Результат
          v-card-text {{ output.join("\r\n") }}

</template>

<script>
  import axios from "axios";


  export default {
    name: 'ExpertSystemIndex',
    data: function () {
      return {
        output: ['123', 'llorem ipsum lorem ipsum lorem ipsum lorem ipsum orem ipsum '],
      }
    },
    async created() {
    },
    methods: {
    }
  }
</script>



