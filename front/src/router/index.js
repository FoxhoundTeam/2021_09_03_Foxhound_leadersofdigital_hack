import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let opts = {
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import('../components/Home.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/login",
      name: "login",
      component: () => import('../components/Login.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/settings",
      name: "Settings",
      component: () => import('../components/Settings.vue'),
      meta: {
        requiresAuth: true
      },
      children: [
        {
          path: "create",
          name: "SettingsCreate",
          component: () => import('../components/modals/ModalSettings.vue'),
          meta: {
            requiresAuth: true
          },
        },
        {
          path: ":id/edit",
          name: "SettingsEdit",
          component: () => import('../components/modals/ModalSettings.vue'),
          meta: {
            requiresAuth: true
          },
        },
      ]
    },
    {
      path: "/files",
      name: "Files",
      component: () => import('../components/Files.vue'),
      meta: {
        requiresAuth: true
      },
    },
  ],
  linkExactActiveClass: 'active'
};
const router = new VueRouter(opts);

export default router
