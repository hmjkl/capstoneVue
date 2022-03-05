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
//export default {
//  data() {
//    return {
//      wellList: null,
//      selectedOption: null,
//      wellData: null,
//    };
//  },
//  watch: {
//    selectedOption: "redrawPlot",
//  },
//  methods: {
//    processUpdate(data) {
//      console.log(data);
//      this.wellData = data.data;
//      this.wellList = data.wellNames;
//    },
//    async fetchData() {
//      const url = "http://localhost:5000/api/proddata"; // @FIXME
//      fetch(url)
//        .then((resp) => resp.json())
//        .then((data) => this.processUpdate(data));
//    },
//    redrawPlot() {
//      if (this.selectedOption.length != 1) {
//        console.error("no well selected.");
//        return;
//      }
//      var selTmp = this.wellData[this.selectedOption];
//      var oilProdPlot = {
//        x: selTmp.date,
//        y: selTmp.oilProd,
//        type: "scatter",
//        name: "Oil Production (m3)",
//      };
//      var steamInjPlot = {
//        x: selTmp.date,
//        y: selTmp.steamInj,
//        type: "scatter",
//        name: "Steam Injection (m3)",
//      };
//      Plotly.newPlot("main-plot", [oilProdPlot, steamInjPlot]);
//    },
//  },
//  created() {
//    //this.fetchData();
//  },
//  components: { FileUploadBox },
//};
</script>

<template>
  <UploadPage v-on:well-data-update="refreshWellData" />
  <Predict :wells="wellList" :wellData="wellData" :modelInfo="modelInfo"/>
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
