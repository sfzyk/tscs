<template>
  <el-card class="applyInfoForm" shadow="always" style="margin: 0 auto;">
    <ApplyInfo ref="applyinfo" :id="id" role="student"></ApplyInfo>
    <div style=" width:75%; background-color:white; margin:0 auto" v-if="projectState === 0">
      <div style="width:50% ; margin:0 auto">
        <upload :proid="id" content="图片" :type="0" :fileList="imglist" :num="5" @refresh="refresh"></upload>
        <upload
          :proid="id"
          content="视频"
          :type="1"
          :fileList="videolist"
          :num="1"
          @refresh="refresh"
        ></upload>
        <upload :proid="id" content="文档" :type="2" :fileList="doclist" :num="1" @refresh="refresh"></upload>
        <el-button @click="submitProj" :v-show="limit">提交</el-button>
        <el-button @click="modifyProj" :v-show="limit">保存</el-button>
      </div>
    </div>
  </el-card>
</template>

<script>
// @ is an alias to /src
import ApplyInfo from "@/components/ApplyInfo.vue";
import api from "@/api/apis";
import upload from "@/components/upload.vue";
import download from "@/components/download.vue";

export default {
  name: "home",
  data() {
    return {
      projectState: 0,
      limit: true,
      imglist: "",
      videolist: "",
      doclist: "",
      intervalID:0
    };
  },
  components: {
    ApplyInfo,
    upload,
    download
  },
  methods: {
    submitProj() {
      this.$refs.applyinfo.submitForm("ruleForm");
    },
    modifyProj() {
      this.$refs.applyinfo.stageInfo();
    },
    refresh() {
      var that = this;
      console.log("refresh")
      api.get_project_image(this.id).then(function(e) {
        that.imglist = e["data"]["data"];
      });
      api.get_project_video(this.id).then(function(e) {
        that.videolist = e["data"]["data"];
      });
      api.get_project_document(this.id).then(function(e) {
        that.doclist = e["data"]["data"];
      });
    }
  },

  created() {
    this.id = this.$route.query.id;
    var that = this;
    api.student_get_project(this.id).then(function(e) {
      var res = JSON.parse(e.data.data);
      that.projectState = res["state"];
      if (that.projectState == "1" || that.projectState == "2") {
        that.limit = true;
      } else if (that.projectState == "0") {
        that.limit = false;
      }
    });
    this.refresh();
    this.intervalID=setInterval(that.modifyProj,60000);
  },
  destroyed(){
    clearInterval(this.intervalID);
  }
};
</script>
<style scoped>
.applyInfoForm {
  width: 75%;
}
</style>
