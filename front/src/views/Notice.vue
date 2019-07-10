<template>
  <div class="inputarea">
    <el-container>
      <el-header>
        <h1 class="texttitle">TSCS科技竞赛管理系统</h1>
      </el-header>
      <el-main>
        <el-input
          type="text"
          style="margin 20px 100px 0 100px;"
          placeholder="请输入通知标题"
          v-model="text"
          maxlength="25"
          show-word-limit
        ></el-input>
        <div style="margin: 20px 0;"></div>
        <el-input
          type="textarea"
          placeholder="请输入通知内容"
          v-model="textarea"
          maxlength="500"
          rows="14"
          show-word-limit
        ></el-input>

        <el-upload
          class="upload-demo"
          ref="upload"
          action="https://jsonplaceholder.typicode.com/posts/"
          :before-remove="beforeRemove"
          :limit="1"
          :on-exceed="handleExceed"
          :file-list="fileList"
          :auto-upload="false"
          :before-upload="beforeUpload"
        >
          <div style="margin-top:19px"></div>
          <el-button size="small" type="primary">上传附件</el-button>
          <div slot="tip" class="el-upload__tip">如果您发布通知时需要附件，请在此处上传</div>
        </el-upload>
        <div style="margin:30px 0"></div>
        <el-button type="primary" @click="submitNotice">发布通知</el-button>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import api from "@/api/apis.js";
export default {
  name: "Notice",
  data() {
    return {
      text: "",
      textarea: "",
      fileList: [],
      submitted: false
    };
  },
  methods: {
    submitNotice() {
      var that = this;
      if (this.text == "" || this.textarea == "") {
        that.$message("请将信息填写完整");
      } else {
        this.$refs.upload.submit();
        console.log("filelistLL" + this.fileList);
        if (!this.submitted) {
          console.log("filelen0");
          api.add_notice(null, this.text, this.textarea).then(function(result) {
            console.log(result);
            that.$message("通知发送成功");
            that.$router.push("/homepage");
          });
        } else {
          this.submitted = false;
        }
        //   api.add_notice(this.text, this.textarea).then(function(e) {
        //   if (e["data"]["data"] == 200) {
        //     that.text = "";
        //     that.textarea = "";
        //     that.$message("通知发布成功");
        //     that.$router.push("/Homepage");
        //   } else if (e["data"]["code"] === 202) {
        //     that.$message("请将信息填写完整！");
        //   }
        // });
      }
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      );
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    beforeUpload(file, fileList) {
      var that = this;
      this.submitted = true;
      api.add_notice(file, this.text, this.textarea).then(function(result) {
        console.log(result);
        that.$router.push("/homepage");
      });
    }
  }
};
</script>

<style scoped>
.inputarea {
  width: 70%;
  margin: 20px auto 10px auto;
  background-color: whitesmoke;
}
.texttitle {
  color: black;
}
</style>
