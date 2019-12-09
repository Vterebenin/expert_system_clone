<template lang="pug">
  v-container
    v-row
      v-col(cols="4")
        v-card()
          v-card-title Рассматривается база: {{ file.name }}
          v-card-text Название файла: {{ file.file }}
          v-card-actions
            v-spacer
            v-btn(@click="handleParseClick") запарсить
      v-col(cols="8")
        v-card
          v-tabs(v-model="tab")
            v-tab Факты
            v-tab Правила
            v-tab Вопросы
          v-tabs-items(v-model="tab")
            v-tab-item
              v-data-table(
                :items="facts"
                :headers="facts_headers"
              )
              pre {{ facts }}
            v-tab-item
              pre {{ rules }}
            v-tab-item
              pre {{ questions }}

</template>

<script>
  import axios from "axios";

  export default {
    name: 'ExpertSystemIndex',
    data: function () {
      return {
        output: ['123', 'llorem ipsum lorem ipsum lorem ipsum lorem ipsum orem ipsum '],
        facts: [],
        facts_headers: [
          {
            text: 'Объект',
            value: 'obj',
          },
          {
            text: 'Атрибут',
            value: 'attribute',
          },
          {
            text: 'Значение',
            value: 'value',
          },
          {
            text: 'Тип',
            value: 'fact_type',
          },
        ],
        rules: [],

        questions: [],
        tab: null
      }
    },
    props: {
      file: {
        required: true,
      }
    },
    async created() {
    },
    methods: {
      async handleParseClick () {
        const {data} = await axios.get(`http://localhost:8000/files/${this.file.id}/parse_file/`)
        const {facts, questions, rules} = data
        console.log(data)
        this.facts = facts
        this.rules = rules
        this.questions = questions
      }
    }
  }
</script>



