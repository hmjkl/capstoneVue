<script>

export default {
  props: {
    maxFileCount: Number,
    target: String,
  },
  data() {
    return {
      fileList: [],
      fileListId: 0,
    };
  },
  methods: {
    // File upload box logic
    onChange(event) {
      this.addToFileList(event.target.files);
    },
    removeFile(file) {
      console.log(file);
      var id = file.id;
      this.fileList = this.fileList.filter((file) => file.id != id);
    },
    dropFile(event) {
      event.preventDefault();
      this.addToFileList(event.dataTransfer.files);
      event.currentTarget.classList.add("bg-gray");
      event.currentTarget.classList.remove("bg-green");
    },
    addToFileList(files) {
      //@FIXME: ensure duplicate files cannot be added
      Array.from(files).forEach((element) =>
        this.fileList.push({ file: element, id: this.fileListId++ })
      );
      this.resizeFileList();
    },
    dragOverFile(event) {
      event.preventDefault();

      if (!event.currentTarget.classList.contains("bg-green")) {
        event.currentTarget.classList.remove("bg-gray");
        event.currentTarget.classList.add("bg-green");
      }
    },
    dragLeave(event) {
      event.preventDefault();
      // if statement needed to prevent flickering
      if (event.target.id === "file-upload") {
        event.currentTarget.classList.add("bg-gray");
        event.currentTarget.classList.remove("bg-green");
      }
    },
    resizeFileList() {
      if (this.fileList.length > this.maxFileCount) {
        this.fileList = this.fileList.slice(
          this.fileList.length - this.maxFileCount
        );
      }
    },
    //processFiles() {
    //  if(this.fileList.length > 0) {
    //    this.$emit("file-process", this.fileList);
    //  }
    //}
    async processFiles() {
      // @FIXME
      console.log(this.target)
      console.log(this.fileList[0]);
      if (this.fileList.length != 1) {
        console.log("fixme");
        return;
      }

      let sendData = new FormData();
      sendData.append("file", this.fileList[0].file);
      fetch(this.target, { method: "POST", body: sendData })
        .then((data) => data.json())
        .then((response) => this.$emit("file-process", response));
    },
  },
};
</script>

<template>
  <div
    id="file-upload"
    class="bg-gray"
    @dragover="dragOverFile"
    @dragleave="dragLeave"
    @drop="dropFile"
  >
    <label>
      <p>
        Drag and drop file, or
        <span class="link">click here</span> to upload file
      </p>
      <input
        type="file"
        id="select-file"
        accept="image/*"
        @change="onChange"
        style="display: none"
      />
    </label>
    <ul class="truncate" v-for="f in fileList" v-bind:key="f.id">
      <li>
        {{ f.file.name }}
        <button @click="removeFile(f)">Remove</button>
      </li>
    </ul>
    <button v-if="this.fileList.length" @click="processFiles">Process</button>
  </div>
</template>

<style>
#file-upload {
  display: flex;
  flex-direction: column;
  padding: 20px;
  width: auto;
  overflow-y: auto;
  text-align: center;
}

.bg-gray {
  background: #cdcdcd;
}

.bg-green {
  background: #00a36c;
}

.link {
  text-decoration: underline;
}

.truncate {
  white-space: nowrap;
  text-overflow: ellipsis;
  list-style-type: none;
}
</style>
