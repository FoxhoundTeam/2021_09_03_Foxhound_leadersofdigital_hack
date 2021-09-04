<template>
  <v-card>
    <v-card-title class="indigo white--text text-h5">
      Файлы найденные в {{ $store.state.pathToFiles }}
    </v-card-title>
    <v-row class="pa-4" justify="space-between">
      <v-col cols="5">
        <v-treeview
          :active.sync="active"
          :open.sync="open"
          :items="dataFiles"
          :loadChildren="loadChildren"
          activatable
          color="success"
          open-on-click
          transition
          item-key="resource_id"
          item-children="_embedded.items"
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
          </v-card>
        </v-scroll-y-transition>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import http from '../http'
function customFilter(object, id) {
  if (
    Object.prototype.hasOwnProperty.call(object, "resource_id") &&
    object["resource_id"] === id
  )
    return object;

  for (var i = 0; i < Object.keys(object).length; i++) {
    if (typeof object[Object.keys(object)[i]] === "object") {
      var o = customFilter(object[Object.keys(object)[i]], id);
      if (o != null) return o;
    }
  }

  return null;
}

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
      dataFiles: [],
      loadingState: false,
    };
  },
  computed: {
    selected() {
      if (!this.active.length) return undefined;

      const id = this.active[0];

      return this.getFile(id);
    },
  },
  methods: {
    async loadChildren(item) {
      return fetch(
        `https://cloud-api.yandex.net/v1/disk/public/resources?public_key=${this.$store.state.pathToFiles}&path=${item.path}`
      )
        .then((res) => res.json())
        .then((json) => {
          for (let data of json._embedded.items) {
            if (data.type === "dir") {
              data._embedded = {
                items: [],
              };
            }
          }
          item._embedded = json._embedded;
        })
        .catch((err) => console.warn(err));
    },
    getFile(id) {
      return customFilter(this.dataFiles, id);
    },
    async loadSelected(selected) {
      this.loadingState = true;
      let response = await http.createItem('Recognize', {
          filename: selected.name,
          url: selected.file,
          inn: this.$store.state.INN,
      }, true)
      let data = response.data;
      selected.new_name = data.new_name;
      selected.code = data.code;
      selected.state = "success";
      this.loadingState = false;
    },
  },
  async beforeMount() {
    if (!this.$store.state.pathToFiles.length) {
      this.$router.replace({ name: "Home" });
    }
    var t = this;
    fetch(
      `https://cloud-api.yandex.net/v1/disk/public/resources?public_key=${this.$store.state.pathToFiles}`
    )
      .then((res) => res.json())
      .then((json) => {
        for (let data of json._embedded.items) {
          if (data.type === "dir") {
            data._embedded = {
              items: [],
            };
          }
        }
        t.dataFiles = [json];
      })
      .catch((err) => console.warn(err));
  },
};
</script>

<style>
</style>