/**
 Vue component for handling file uploads and settings for CSV headers.
 */
<script>
import natsort from "natsort";
import FileUploadBox from "./fileUploadBox.vue";

export default {
  data() {
    return {
      csvHeaderSelection: {
        wellNames: null,
        date: null,
        oilProd: null,
        steamInj: null,
        waterProd: null
      },
      csvHeaderNames: ['WP', 'DATE', 'OP', 'SI', 'WP'],
      fileUpdated: 0,
    };
  },
  watch: {
  },
  methods: {
    processUpdate(data) {

      Object.keys(data.data).forEach(key =>
      data.data[key].date = data.data[key].date.map(date => new Date(date))
      )
      console.log(data.data)
      this.$emit('well-data-update', data)
    },
    updateHeaderSelection(val, key) {
      this.csvHeaderSelection[key] = event.target.value
      console.log(this.csvHeaderSelection)
    }
  },
  created() {
  },
  computed: {
    requiredHeaderAliases() {
      return [
        { key: "wellNames", label: "Well Names" },
        { key: "date", label: "Dates" },
        { key: "oilProd", label: "Oil Production" },
        { key: "steamInj", label: "Steam Injection" },
        { key: "waterProd", label: "Water Production" }
      ]
    }
  },
  components: { FileUploadBox },
};
</script>

<template>
  <div class="content">
    <FileUploadBox
      :maxFileCount="1"
      target="http://localhost:5000/api/csv-transform"
      v-on:file-process="processUpdate"
    ></FileUploadBox>
  </div>

  <!-- @FIXME: Consider replacing v-on:change w/ some form of watcher. -->
  <!-- <div v-if="fileUpdated" v-for="header in requiredHeaderAliases">
    {{ header.label }}:
    <select v-model="csvHeaderSelection[header.key]">
      <option v-for="option in csvHeaderNames">{{ option }}</option>
    </select>
  </div> -->
</template>

<!--
<style>
.content {
  display: flex;
}

.left {
}

.right {
}

</style>
-->
