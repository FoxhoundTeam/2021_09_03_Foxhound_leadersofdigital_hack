<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-text-field
          label="Введите ссылку на диск"
          rounded
          outlined
          v-model="pathToFiles"
        ></v-text-field>
        <v-text-field
          label="Введите ИНН"
          rounded
          outlined
          v-model="INN"
        ></v-text-field>
        <v-btn
          @click="$router.replace({ name: 'Files' })"
          block
          :disabled="!$store.state.pathToFiles.length"
          >Продолжить</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
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