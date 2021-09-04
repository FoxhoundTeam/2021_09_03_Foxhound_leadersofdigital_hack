<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-tabs class="mb-4" v-model="tab" align-with-title>
          <v-tabs-slider></v-tabs-slider>

          <v-tab> Папка </v-tab>
          <v-tab> Ссылка </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item>
            <upload-folder class="mt-3" />
          </v-tab-item>
          <v-tab-item>
            <v-text-field
              class="mt-3"
              label="Введите ссылку на диск"
              rounded
              outlined
              v-model="pathToFiles"
            ></v-text-field>
          </v-tab-item>
        </v-tabs-items>
        <v-text-field
          label="Введите ИНН"
          rounded
          outlined
          v-model="INN"
          counter
          maxlength="10"
        ></v-text-field>
        <v-btn
          @click="$router.replace({ name: 'Files' })"
          block
          :disabled="
            (!$store.state.pathToFiles.length && !$store.state.tree) ||
            !$store.state.INN.length
          "
          >Продолжить</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UploadFolder from "./UploadFolder.vue";
export default {
  components: { UploadFolder },
  data() {
    return {
      files: [],
      tab: null,
    };
  },
  watch: {
    files() {
      console.log(this.files);
    },
  },
  computed: {
    pathToFiles: {
      get() {
        return this.$store.state.pathToFiles;
      },
      set(value) {
        this.$store.commit("setPathToFiles", value);
      },
    },
    INN: {
      get() {
        return this.$store.state.INN;
      },
      set(value) {
        this.$store.commit("setINN", value);
      },
    },
  },
};
</script>

<style>
</style>