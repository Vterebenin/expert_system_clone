<template lang="pug">
  v-row
    v-col(offset="2" cols="8")
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
                v-text-field(v-model="name" color="accent" name="name" label="Введите название базы знаний")
                v-file-input(v-model="file" color="accent" name="file" label="Загрузить файл с базой знаний")
              v-card-actions
                v-spacer
                v-btn(type="submit") Загрузить
        v-tab-item
          v-card
            v-card-title Выберите базу знаний
            v-divider
            v-card-text
              v-list(v-if="files.length")
                v-radio-group(v-model="selected_file")
                  v-list-item(v-for="(f, i) in files" :key="f.id")
                    v-radio(:value="f")
                      template(#label)
                        span.file_name
                          b {{ f.name }}:
                          | &nbsp;{{ decodeUtf8(f.file) }}
                    v-icon(@click="handleDeleteClick(f.id)") mdi-delete
              v-list(v-else)
                v-list-item К сожалению, базы знаний отсутствуют
            v-card-actions
              v-spacer
              v-btn(:disabled="!files.length || !selected_file" @click="handleSelectFileClick") Выбрать
</template>

<script>
  import axios from "axios";

  export default {
    name: 'Main',
    data: function () {
      return {
        tab: null,
        files: [],
        name: '',
        file: [],
        file_name: '',
        file_url: '',
        selected_file: '',
        nameRules: [
          v => !!v || 'Имя обязательно',
          v => (v && v.length <= 20 && v.length > 3) || 'Имя должно быть длинной от 3 до 10 символов',
        ],
        fileRules: [
          v => !!v || 'Файл обязателен',
        ],
      }
    },
    async created() {
      this.updateFiles()

    },
    methods: {
      async getFormValues() {
        let form_data = new FormData()
        form_data.append('file', this.file)
        form_data.append('name', this.name)
        // console.log(submitEvent)
        await axios.post('http://localhost:8000/files/', form_data)
        this.updateFiles()
        this.tab = 1
      },
      decodeUtf8 (s) {
        const str = decodeURIComponent(`${s}`).split('/')
        return str[str.length-1]
      },
      async updateFiles() {
        const { data } = await axios.get('http://localhost:8000/files/')
        this.files = data
      },
      async handleDeleteClick(id) {
        await axios.delete(`http://localhost:8000/files/${id}/`)
        this.updateFiles()
      },
      handleSelectFileClick() {
        console.log(this.selected_file)
        this.$emit('select', this.selected_file)
      }
    },
  }
</script>
<style scoped lang="scss">
  .file_name {
    font-size: 12px;
  }
  .take_link {
    text-decoration: none;
  }

</style>



