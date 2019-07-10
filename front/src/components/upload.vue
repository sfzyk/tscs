<template>
  <el-upload
    class="upload-demo"
    action
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :before-remove="beforeRemove"
    multiple
    :limit="num"
    :before-upload="beforeupload"
    :on-exceed="handleExceed"
    :file-list="fileList"
    :http-request="request"
    :accept="accepts[type]"
    
  >
    <el-button size="small" type="primary">点击上传{{content}}</el-button>
    <div slot="tip" class="el-upload__tip">只能上传{{accepts[type]}}文件，且不超过{{num}}个</div>
  </el-upload>
</template> 
<script>
import api from "@/api/apis.js";
import axios from "@/api/http.js";
import { type } from "os";
export default {
  name: "upload",
  props: {
    proid: Number,
    content: String,
    type: Number,
    fileList: Array,
    num: Number
  },
  data() {
    return {
      //fileList: [],
      accepts: [".jpg,.png", ".flv,.avi,.mp4", ".pdf"],
      types: ["image", "video", "document"]
    };
  },
  methods: {
    change() {},
    handleRemove(file, fileList) {
      var num = file["id"];
      var that = this;
      switch (this.type) {
        case 0:
          api.delete_image(num).then(function(result) {
            switch (result["data"]["code"]) {
              case 200:
                that.$message({
                  message: "删除成功！",
                  type: "success"
                });
                that.$emit("refresh");
                break;
              case 273:
                that.$message.error("文件不存在！");
            }
          });
          break;
        case 1:
          api.delete_video(num).then(function(result) {
            console.log("result");
            console.log(result);
            switch (result["data"]["code"]) {
              case 200:
                that.$message({
                  message: "删除成功！",
                  type: "success"
                });
                that.$emit("refresh");
                break;
              case 273:
                that.$message.error("文件不存在！");
            }
          });
          break;
        case 2:
          api.delete_document(num).then(function(result) {
            console.log("result");
            console.log(result);
            switch (result["data"]["code"]) {
              case 200:
                that.$message({
                  message: "删除成功！",
                  type: "success"
                });
                that.$emit("refresh");
                break;
              case 273:
                that.$message.error("文件不存在！");
            }
          });
      }
    },
    handlePreview(file) {
      console.log(this.types[this.type]);
      api.fileview(this.types[this.type], file["id"]);
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 ${this.num} 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      );
      0;
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    request(req) {
      console.log(req);
    },
    progress(file, fileList) {},
    beforeupload(file) {
      var that = this;
      that.$message({
                  message: "开始上传"
                });
      switch (this.type) {
        case 0:
          api.add_image(file, this.proid).then(function(result) {
            that.$emit("refresh");
            that.$message({
              message: "上传成功！",
              type: "success"
            });
          });
          break;
        case 1:
          api.add_video(file, this.proid).then(function(result) {
            that.$emit("refresh");
            that.$message({
              message: "上传成功！",
              type: "success"
            });
          });
          break;
        case 2:
          api.add_document(file, this.proid).then(function(result) {
            that.$emit("refresh");
            that.$message({
              message: "上传成功！",
              type: "success"
            });
          });
          break;
      }
    }
  }
};
</script>
