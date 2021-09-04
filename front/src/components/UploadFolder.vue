<template>
  <v-file-input
    label="Выберите папку"
    :webkitdirectory="uploadDir"
    :mozdirectory="uploadDir"
    v-model="files"
    multiple
    @change="setFiles"
  ></v-file-input>
</template>

<script>
const AVAILABLE_TYPES = [
  "application/pdf",
  "application/vnd.ms-excel",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
];

export default {
  props: {
    title: {
      type: String,
    },
    value: {
      type: Array,
    },
    uploadDir: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      files: [],
    };
  },
  methods: {
    setFiles() {
      let files = [];
      var ind = 0;
      for (let file of this.files) {
        let splitedPath = file.webkitRelativePath.split("/");
        var prev_folder = undefined;
        var folder = undefined;
        if (splitedPath.length > 2) {
          prev_folder =
            files[
              files.findIndex(
                (v) => v.name == splitedPath[1] && v.type == "dir"
              )
            ];
          if (!prev_folder) {
            prev_folder = {
              name: splitedPath[1],
              type: "dir",
              items: [],
              resource_id: ind,
            };
            files.push(prev_folder);
            ind += 1;
          }
          for (let path of splitedPath.slice(2, splitedPath.length - 1)) {
            folder =
              prev_folder.items[
                prev_folder.items.findIndex(
                  (v) => v.name == path && v.type == "dir"
                )
              ];
            if (!folder) {
              folder = {
                name: path,
                type: "dir",
                items: [],
                resource_id: ind,
              };
              prev_folder.items.push(folder);
              ind += 1;
            }
            prev_folder = folder;
          }
        }
        let fileObj = {
          name: file.name,
          file: file,
          mime_type: file.type,
          resource_id: ind,
          size: file.size,
        };
        if (prev_folder) {
          prev_folder.items.push(fileObj);
        } else {
          files.push(fileObj);
        }
        ind += 1;
        if (AVAILABLE_TYPES.findIndex((v) => v === fileObj.mime_type) != -1) {
          this.$store.commit("addFile", fileObj);
          fileObj.recogniziable = true;
        }
      }
      this.$store.commit("setTree", files);
    },
  },
};
</script>

<style>
</style>