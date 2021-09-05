<template>
  <v-card>
    <v-toolbar extended dark color="primary">
      <v-toolbar-title
        >Файлы найденные в {{ $store.state.pathToFiles || "загруженной папке" }}
      </v-toolbar-title>
      <template #extension>
        <v-toolbar-title v-if="!loadingAllState"
          >Для распознавания доступно
          {{ $store.state.filesToRecognize.length }} файлов</v-toolbar-title
        >
        <v-toolbar-title v-else
          >Распознаем документы... Распознано {{ recognized.length }} из
          {{ $store.state.filesToRecognize.length }} файлов, не распознано
          {{ unrecognized.length }}</v-toolbar-title
        >
        <v-progress-linear
          :active="loadingAllState"
          absolute
          bottom
          :indeterminate="!(recognized.length + unrecognized.length)"
          v-model="loadProgress"
          :query="true"
          color="white"
        ></v-progress-linear
      ></template>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn
          dark
          text
          @click="loadAll"
          :disabled="!$store.state.filesToRecognize.length || loadingAllState"
          >Распознать все</v-btn
        >
      </v-toolbar-items>
    </v-toolbar>

    <v-row class="pa-4" justify="space-between">
      <v-col cols="5">
        <v-treeview
          :active.sync="active"
          :open.sync="open"
          :items="$store.state.tree"
          activatable
          color="success"
          open-on-click
          transition
          item-key="resource_id"
          item-children="items"
        >
          <template v-slot:prepend="{ item, open }">
            <v-icon v-if="item.type === 'dir'">
              {{ open ? "mdi-folder-open" : "mdi-folder" }}
            </v-icon>
            <v-icon v-else>
              {{ files[item.mime_type] }}
            </v-icon>
          </template>
        </v-treeview>
      </v-col>

      <v-divider vertical></v-divider>

      <v-col class="d-flex text-center">
        <v-scroll-y-transition mode="out-in">
          <div
            v-if="!selected"
            class="text-h6 grey--text text--lighten-1 font-weight-light"
            style="align-self: center"
          >
            Выберите файл для просмотра информации
          </div>
          <v-card
            v-else
            :key="selected.id"
            class="pt-6 mx-auto"
            flat
            max-width="600"
          >
            <v-card-text>
              <v-avatar size="88">
                <v-icon>
                  {{ files[selected.mime_type] }}
                </v-icon>
              </v-avatar>
              <h3 class="text-h5 mb-2">
                {{ selected.name }}
              </h3>
            </v-card-text>
            <v-divider></v-divider>
            <v-row
              class="text-left my-0 py-0"
              tag="v-card-text"
              v-if="selected.code"
            >
              <v-col class="text-right mr-4 my-0" tag="strong" cols="5">
                Новое название:
              </v-col>
              <v-col>{{ selected.new_name }}</v-col>
              <v-col class="text-right mr-4 my-0" tag="strong" cols="5">
                Код номенклатуры:
              </v-col>
              <v-col>{{ selected.code }}</v-col>
            </v-row>
            <v-row class="text-left my-0 py-0" tag="v-card-text">
              <v-col class="text-right mr-4 my-0" tag="strong" cols="5">
                Тип файла:
              </v-col>
              <v-col>{{ types[selected.mime_type] }}</v-col>
            </v-row>
            <v-row class="text-left my-0 py-0" tag="v-card-text">
              <v-col class="text-right mr-4 my-0" tag="strong" cols="5">
                Размер:
              </v-col>
              <v-col>
                {{ selected.size }}
              </v-col>
            </v-row>
            <v-row
              block
              v-if="
                available_types.findIndex((v) => v === selected.mime_type) !=
                  -1 && selected.state !== 'success'
              "
            >
              <v-col cols="12">
                <v-btn
                  :loading="Boolean(loadingState)"
                  :disabled="Boolean(loadingState)"
                  color="primary"
                  @click="loadSelected(selected)"
                  >Распознать документ
                  <v-icon right dark> mdi-eye </v-icon></v-btn
                >
                <v-divider v-if="loadingState"></v-divider>
                <v-progress-linear
                  v-if="loadingState"
                  indeterminate
                  color="primary"
                ></v-progress-linear>
                <span v-if="loadingState">Распознаём документ</span>
              </v-col>
            </v-row>
            <v-row v-if="selected.state === 'success'">
              <v-col cols="12">
                <v-alert type="success"
                  >Документ успешно распозан и отправлен в систему</v-alert
                >
              </v-col>
            </v-row>
            <v-row v-else-if="selected.state === 'warning'">
              <v-col cols="12">
                <v-alert type="warning">{{ selected.message }}</v-alert>
              </v-col>
            </v-row>
          </v-card>
        </v-scroll-y-transition>
      </v-col>
    </v-row>
    <v-overlay class="text-center" :value="$store.state.loadingFiles">
      <p v-if="$store.state.loadingFiles">Загружаем файлы с диска. Подождите</p>
      <p v-else>Распознаём файлы. Подождите</p>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      files: {
        "application/pdf": "mdi-file-pdf",
        "application/vnd.ms-excel": "mdi-file-excel",
        "text/plain": "mdi-file-document-outline",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
          "mdi-file-excel",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
          "mdi-file-word",
      },
      types: {
        "application/pdf": "pdf",
        "application/vnd.ms-excel": "Microsoft excel",
        "text/plain": "txt",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
          "Microsoft excel",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
          "Microsoft word",
      },
      available_types: [
        "application/pdf",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ],
      active: [],
      open: [],
      loadingState: false,
      loadingAllState: false,
      recognized: [],
      unrecognized: [],
    };
  },
  computed: {
    selected() {
      if (!this.active.length) return undefined;

      const id = this.active[0];

      return this.$store.getters.getFile(id);
    },
    loadProgress() {
      return ((this.recognized.length + this.unrecognized.length) / (this.$store.state.filesToRecognize.length || 1)) * 100;
    },
  },
  methods: {
    async loadSelected(selected) {
      this.loadingState = true;
      let response = await this.recognize(selected);
      if (response.status == 200 && response.data.code) {
        let data = response.data;
        selected.new_name = data.new_name;
        selected.code = data.code;
        selected.state = "success";
      } else {
        selected.state = "warning";
        selected.message = response.data.status;
      }
      this.loadingState = false;
    },
    async loadAll() {
      this.loadingAllState = true;
      this.recognized = [];
      this.unrecognized = [];
      for (let file of this.$store.state.filesToRecognize) {
        let response = await this.recognize(file);
        let selected = this.$store.getters.getFile(file.resource_id);
        if (response.status == 200 && response.data.code) {
          let data = response.data;
          selected.new_name = data.new_name;
          selected.code = data.code;
          selected.state = "success";
          this.recognized.push(selected);
        } else {
          selected.state = "warning";
          selected.message = response.data.status;
          this.unrecognized.push(selected);
        }
      }
      this.loadingAllState = false;
    },
    async recognize(data) {
      let payload = {
        filename: data.name,
        inn: this.$store.state.INN,
      };
      if (data.file instanceof File) {
        payload.file = data.file;
      } else {
        payload.url = data.file;
      }
      var form = new FormData();
      for (let key in payload) {
        form.append(key, payload[key]);
      }
      try {
        return await axios.post("/rest_api/setting/recognize/", form, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      } catch (error) {
        this.$showErrorModal(error.response.data);
      }
    },
  },
  async beforeMount() {
    if (
      !this.$store.state.pathToFiles.length &&
      !this.$store.state.tree.length
    ) {
      this.$router.replace({ name: "Home" });
      return;
    }
    if (!this.$store.state.tree.length) {
      await this.$store.dispatch("getFiles");
    }
  },
};
</script>

<style>
</style>