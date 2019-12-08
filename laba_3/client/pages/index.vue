<template lang="pug">
  v-container
    v-row
      v-col.text-center(cols="12")
        | Expert System Clone
    v-row
      v-col(cols="6")
        v-tabs(grow v-model="tab" color="white")
          v-tab Загрузить
          v-tab Выбрать из сохраненных
        v-tabs-items(v-model="tab")
          v-tab-item
            v-card
              v-card-title Загрузите базу знаний
              v-divider
              v-form(@submit.prevent="getFormValues")
                v-card-text
                  v-text-field(v-model="name" name="name" label="Введите название базы знаний")
                  v-file-input(v-model="file" name="file" label="Загрузить файл с базой знаний")
                v-card-actions
                  v-spacer
                  v-btn(type="submit") Загрузить
          v-tab-item
            v-card
              v-card-title Выберите базу знаний
              v-divider
              v-form
                v-card-text
                  v-list(v-if="files.length")
                    v-list-item(v-for="(file, i) in files" :key="i")
                  v-list(v-else)
                    v-list-item К сожалению, базы знаний отсутствуют

                v-card-actions
                  v-spacer
                  v-btn(typ="submit") Выбрать
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
        tab: null,
        files: [],
        output: ['123', 'llorem ipsum lorem ipsum lorem ipsum lorem ipsum orem ipsum '],
        name: '',
        file: [],
        file_name: '',
        file_url: '',

      }
    },
    methods: {
      async getFormValues(submitEvent) {
        let form_data = new FormData()
        form_data.append('file', this.file)
        form_data.append('name', this.name)
        // console.log(submitEvent)
        console.log(this.file)
        const { data } = await axios.post('http://localhost:8000/files/', form_data)

      }
    }

  }
</script>
