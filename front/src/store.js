import Vuex from 'vuex'
import http from './http'
import Axios from 'axios'
import Vue from 'vue'

const AVAILABLE_TYPES = [
    "application/pdf",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]

Vue.use(Vuex)

function customFilter(object, id) {
    if (Object.prototype.hasOwnProperty.call(object, 'resource_id') && object["resource_id"] === id)
        return object;

    for (var i = 0; i < Object.keys(object).length; i++) {
        if (typeof object[Object.keys(object)[i]] === "object") {
            var o = customFilter(object[Object.keys(object)[i]], id);
            if (o != null)
                return o;
        }
    }

    return null;
}

async function recursiveTreeFromDiskBuilder(context, path, object) {
    if (object.type !== 'dir') {
        if (AVAILABLE_TYPES.findIndex((v) => v === object.mime_type) !=
            -1) {
            context.commit('addFile', object);
            object.recogniziable = true;
        }
        return object;
    }
    object = await (await fetch(
        `https://cloud-api.yandex.net/v1/disk/public/resources?public_key=${path}&path=${object.path}`
    )).json()
    let items = [];
    for (var item of object._embedded.items) {
        item = await recursiveTreeFromDiskBuilder(context, path, item);
        items.push(item)
    }
    object.items = items
    return object;
}


const store = new Vuex.Store({
    state: {
        user: null,
        isAuthenticated: false,
        settings: [],
        pathToFiles: "",
        INN: "",
        tree: [],
        loadingFiles: false,
        filesToRecognize: [],
    },
    getters: {
        getFile: state => id => {
            return customFilter(state.tree, id);
        }
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuthenticated(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setPathToFiles(state, data) {
            state.pathToFiles = data;
        },
        setINN(state, data) {
            state.INN = data;
        },
        setSettings(state, settings) {
            state.settings = settings;
        },
        setTree(state, tree) {
            state.tree = tree;
        },
        setLoadingFiles(state, loading) {
            state.loadingFiles = loading;
        },
        addFile(state, file) {
            state.filesToRecognize.push(file);
        }
    },
    actions: {
        async getSettings(context) {
            let settings = (await http.getList('Setting', {}, true)).data;
            context.commit('setSettings', settings);
        },
        async getFiles(context) {
            context.commit('setLoadingFiles', true);
            let root = await (await fetch(
                `https://cloud-api.yandex.net/v1/disk/public/resources?public_key=${context.state.pathToFiles}`
            )).json()
            context.commit('setTree', root._embedded.items);
            root = await recursiveTreeFromDiskBuilder(context, context.state.pathToFiles, root);
            context.commit('setTree', root.items);
            context.commit('setLoadingFiles', false);
        },
        async addItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let response = (await http.createItem(data.url, item_data, true)).data;
            let items = context.state[data.items_name]
            items.push(response);
            context.commit(mutation, items);
        },
        async updateItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let dataID = data.dataID;
            let response = (await http.updateItem(data.url, dataID, item_data, true)).data;
            let items = context.state[data.items_name]
            let index = items.findIndex(v => v.id == dataID);
            if (index != -1) {
                Vue.set(items, index, response);
            }
            context.commit(mutation, items);
        },
        async login(context, creds) {
            var username = creds.username;
            var password = creds.password;
            var reg_exp_mail = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/
            var login_info = {
                email: username,
                password: password
            }
            if (username.match(reg_exp_mail) != null) {
                login_info = {
                    email: username,
                    password: password
                }
            } else {
                login_info = {
                    username: username,
                    password: password
                }
            }
            var status = false;
            try {
                await (Axios.post("/rest_api/auth/login/", login_info));
                status = true;
            } catch (error) {
                var data = error.response.data;
                if (data.non_field_errors) {
                    Vue.showErrorModal(data.non_field_errors);
                } else {
                    var result = '';
                    for (var k in data) {
                        result += `${k}: ${data[k]}\n`
                    }
                    Vue.showErrorModal(result);
                }
            }
            Axios.defaults.headers.common['X-CSRFToken'] = Vue.$cookies.get('csrftoken');
            await context.dispatch('checkAuth');
            return status;
        },
        async logout(context) {
            await Axios.post("/rest_api/auth/logout/");
            context.commit('setAuthenticated', false);
            context.commit('setUser', {});
            Axios.defaults.headers.common['X-CSRFToken'] = Vue.$cookies.get('csrftoken');
        },
        async checkAuth(context) {
            try {
                var result = await Axios.get("/rest_api/auth/user/");
                if (result.status != 200) {
                    context.commit('setUser', {});
                    return
                }
                context.commit('setAuthenticated', true);
                context.commit('setUser', result.data);
                Axios.defaults.headers.common['X-CSRFToken'] = Vue.$cookies.get('csrftoken');
            } catch (e) {
                context.commit('setUser', {});
            }
        },
    }
})

export default store;
