<template>
  <div>
    <v-data-table
      :loading="loading"
      disable-sort
      class="elevation-1"
      :items="$store.state.settings"
      :headers="headers"
      @click:row="
        (row) =>
          $router.push({
            name: 'SettingsEdit',
            query: {
              ...$route.query,
            },
            params: {
              id: row.id,
            },
          })
      "
      :search="search"
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="6">
            <v-toolbar-title class="ml-5 mt-3"
              >Настройки критериев</v-toolbar-title
            >
          </v-col>
          <v-col cols="6">
            <div class="d-flex align-items-center justify-content-end">
              <v-text-field
                prepend-icon="search"
                label="Поиск"
                v-model="search"
              ></v-text-field>
              <v-tooltip bottom open-delay="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mx-1"
                    v-bind="attrs"
                    v-on="on"
                    icon
                    @click="
                      $router.push({
                        name: 'SettingsCreate',
                        query: {
                          ...$route.query,
                        },
                      })
                    "
                  >
                    <v-icon color="gray" v-bind="attrs" v-on="on"> add </v-icon>
                  </v-btn>
                </template>
                <span>Добавить</span>
              </v-tooltip>
            </div>
          </v-col>
        </v-row>
      </template>
      <template #item.criterias="{ item }">
        <v-chip-group column>
          <v-chip
            v-for="(criteria, i) in item.criterias"
            :key="criteria + String(i)"
          >
            {{ criteria.text }}
          </v-chip>
        </v-chip-group>
      </template>
    </v-data-table>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "Наименование по номенклатуре (корректное)",
          value: "name",
        },
        {
          text: "Коды номенклатур документов",
          value: "code",
        },
        {
          text: "Формат",
          value: "type",
        },
        {
          text: "Критерии для распознования документа",
          value: "criterias",
          filterable: false,
        },
      ],
      loading: true,
      search: "",
    };
  },
  async beforeMount() {
    this.loading = true;
    if (this.$store.state.settings.length == 0) {
      await this.$store.dispatch("getSettings");
    }
    this.loading = false;
  },
};
</script>

<style>
</style>