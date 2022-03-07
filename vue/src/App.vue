<script>
// @FIXME: use better version of plotly to lower page size
import UploadPage from "./uploadPage.vue";
import Predict from "./predict.vue"
import natsort from "natsort"

export default {
  components: { UploadPage, Predict },
  data() {
    return {
      wellList: undefined,
      wellData: undefined,
      modelInfo: undefined,
    }
  },
  methods: {
    async getModelInfo() {
      const url = "http://localhost:5000/api/model-info";
      return fetch(url).then(resp => resp.json()).then(obj => this.modelInfo = obj);
    },
    refreshWellData(data) {

      if (data === null || data === undefined) {
        console.error('JSON well data response from server not valid');
        return;
      }

      this.wellData = data.data;
      this.wellList = data.wellNames.sort(natsort());

    }
  },
  created() {
    this.getModelInfo();
    //this.modelInfo = this.getModelInfo();
    //console.log(this.modelInfo);
  }
}

</script>

<template>
  <UploadPage v-on:well-data-update="refreshWellData" />
  <Predict :wells="wellList" :wellData="wellData" :modelInfo="modelInfo"/>
</template>