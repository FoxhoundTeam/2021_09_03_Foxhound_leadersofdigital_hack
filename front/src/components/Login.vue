<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12"><h1>Foxhound</h1></b-col>
    </b-row>
    <b-row>
      <b-col class="my-1" sm="7" order-sm="1" order="12"
        >
        <!-- <b-img class="w-75" :src="hackLogo"></b-img> -->
        <h3 class="mt-2">
          Веб-приложение для распознования документов.
        </h3></b-col
      >
      <b-col class="my-1" order-sm="12" order="1" sm="5">
        <b-card>
          <v-text-field label='Логин' v-model="username"></v-text-field>
          <v-text-field label='Пароль' v-model="password" type="password"></v-text-field>
          <v-checkbox v-model="remember" class="md-primary" label='Запомнить меня'/>
          <v-btn @click="login" block color="primary">Войти</v-btn>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      remember: false,
    };
  },
  methods: {
    async login() {
      await this.$store.dispatch("login", {
        username: this.username,
        password: this.password,
      });
      this.$router.replace({ name: "Home" });
    },
  },
  beforeMount() {
    if (this.$store.state.isAuthenticated) {
      this.$router.replace({ name: "Home" });
    }
  },
};
</script>

<style>
.temp {
  width: 80px;
}
</style>