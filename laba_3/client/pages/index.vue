<template lang="pug">
  v-container
    v-row
      v-col.text-center(cols="12")
        | Expert System Clone
    Kdb_parse(v-if="selected_file")
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



