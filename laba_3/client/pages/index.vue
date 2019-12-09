<template lang="pug">
  v-container
    v-row
      v-col.text-center(cols="12")
        v-icon.float-left(@click="selected_file = ''" v-if="selected_file") mdi-close
        | Expert System Clone
    Kdb_parse(v-if="selected_file" :file="selected_file" @clear="selected_file = ''")
    Main(v-else @select="selected_file = $event")

</template>

<script>
  import Main from "../components/main";
  import Kdb_parse from "../components/kdb_parse";

  export default {
    name: 'ExpertSystemIndex',
    components: { Main, Kdb_parse },
    data: function () {
      return {
        selected_file: '',
      }
    },
    async created() {
    },
    methods: {
    }
  }
</script>



