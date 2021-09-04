<template>
  <v-dialog v-model="show" max-width="800px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">{{
            `${
              this.$route.params.id ? "Редактировать" : "Создать"
            } настройки критериев`
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="settings.name"
            label="Наименование по номенклатуре (корректное)"
            counter
            maxlength="256"
          ></v-text-field>
          <v-text-field
            v-model="settings.code"
            label="Коды номенклатур документов"
            counter
            maxlength="64"
          ></v-text-field>
          <v-select
            :items="formats"
            v-model="settings.type"
            label="Формат"
          ></v-select>
          <v-container>
            <v-row v-for="(tag, i) in settings.criterias" :key="i">
              <v-col class="my-0 py-0" cols="4">
                <v-select
                  :items="types"
                  v-model="settings.criterias[i].type"
                  rounded
                  filled
                  item-text="name"
                  item-value="value"
                ></v-select>
              </v-col>
              <v-col class="my-0 py-0" cols="8">
                <v-text-field
                  rounded
                  filled
                  append-icon="delete"
                  @click:append="deleteItem(i)"
                  v-model="settings.criterias[i].text"
                >
                </v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                ><v-btn class="mx-1" icon @click="addItem()">
                  <v-icon color="gray"> add </v-icon>
                </v-btn></v-col
              >
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeModal()">
            Закрыть
          </v-btn>
          <v-btn color="blue darken-1" text @click="save()">
            {{ $route.params.id ? "Сохранить" : "Создать" }}
          </v-btn>
        </v-card-actions>
      </template>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data() {
    return {
      formats: ["xlsx", "pdf", "xls"],
      types: [
        {
          name: "Регулярное выражение",
          value: "r",
        },
        {
          name: "Строка",
          value: "s",
        },
      ],
      settings: { name: "", criterias: [] },
    };
  },
  computed: {
    show() {
      return (
        this.$route.name == "SettingsEdit" ||
        this.$route.name == "SettingsCreate"
      );
    },
  },
  beforeMount() {
    this.settings = {
      ...(this.$store.state.settings[
        this.$store.state.settings.findIndex(
          (v) => v.id == this.$route.params.id
        )
      ] || this.settings),
    };
  },
  methods: {
    closeModal() {
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "Settings",
        query: q,
      });
    },
    async save() {
      if (this.settings.id) {
        await this.$store.dispatch("updateItem", {
          data: this.settings,
          dataID: this.settings.id,
          mutation: "setSettings",
          url: "Setting",
          items_name: "settings",
        });
      } else {
        await this.$store.dispatch("addItem", {
          data: this.settings,
          mutation: "setSettings",
          url: "Setting",
          items_name: "settings",
        });
      }
      this.closeModal();
    },
    addItem() {
      let criterias = [...this.settings.criterias];
      criterias.push({ type: "s", text: "" });
      this.$set(this.settings, "criterias", criterias);
    },
    deleteItem(ind) {
      this.settings.criterias.splice(ind, 1);
    },
  },
};
</script>
<style>
</style>