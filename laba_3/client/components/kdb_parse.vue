<template lang="pug">
  v-container
    v-row
      v-col(cols="4")
        v-card()
          v-card-title Рассматривается база: {{ file.name }}
          v-card-text Название файла: {{ file.file }}
      v-col(cols="8")
        v-card
          v-tabs(grow v-model="tab")
            v-tab Факты
            v-tab Таргетный факт
          v-tabs-items(v-model="tab")
            v-tab-item
              v-data-table(
                v-model="initial_facts"
                show-select
                item-key="id"
                :items="facts"
                :headers="facts_headers"
              )
            v-tab-item
              v-card.elevation-0(tile)
                v-card-text
                  v-select(
                    v-model="target_fact_id"
                    name="fact"
                    label="Выберите факт для проверки"
                    item-text="value"
                    item-value="id"
                    :items="target_facts")
                v-card-actions
                  v-spacer
                  v-btn(:disabled="!target_fact_id" @click="check_fact") проверить факт
              v-divider
              v-col
                | Результаты:
              v-col.ws-pw(v-if="output.length") {{ output.join('\r\n') }}
              v-col.ws-pw(v-else) Проверка не запущена или обрабатывается

</template>

<script>
  import axios from "axios";

  export default {
    name: 'ExpertSystemIndex',
    data: function () {
      return {
        output: [],
        facts: [],
        initial_facts: [],
        target_facts: [],
        target_fact_id: '',
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
      this.handleParse()
    },
    methods: {
      async handleParse () {
        const {data} = await axios.get(`http://localhost:8000/files/${this.file.id}/parse_file/`)
        const {facts, questions, rules} = data
        console.log(data)
        for (let f of facts) {
          if (f.fact_type === 'Изначальный') this.initial_facts.push(f)
          if (f.fact_type === 'Финальный') this.target_facts.push(f)
        }
        this.facts = facts
        this.rules = rules
        this.questions = questions
      },
      async check_fact () {
        console.log(this.initial_facts)
        console.log(this.target_fact_id)
        const { file, facts, initial_facts, target_fact_id } = this
        const { data } = await axios
          .post(`http://localhost:8000/files/${file.id}/check_fact/`, {
            facts,
            initial_facts,
            target_fact_id
          })
        console.log(data)
        this.output = data

      }

    }
  }
</script>
<style>
  .ws-pw {
    white-space: pre-wrap;
    font-size: 12px;

  }
</style>



