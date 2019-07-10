<template>
  <el-card class="applyInfoForm" shadow="always" style="margin: 0 auto;">
    <ApplyInfo ref="applyinfo" :id="id" role="admin"></ApplyInfo>
    <ProjectExpert :state='this.state' :proId="this.id" :expTags='this.expTags'></ProjectExpert>
    <comments :proId="id"></comments>
    <el-button @click="passProj" :disabled="projectState">通过</el-button>
    <el-button @click="backProj" :disabled="projectState">退回</el-button>
  </el-card>
</template>

<script>
// @ is an alias to /src
import ApplyInfo from "@/components/ApplyInfo.vue";
import ProjectExpert from "@/components/ProjectExpert.vue";
import comments from "@/components/comments.vue"
import api from "@/api/apis";
export default {
  name: "home",
  data() {
    return {
      projectState: true,
      state: 0,
      expTags: []
    };
  },
  components: {
    ApplyInfo,
    ProjectExpert,
    comments
  },
  methods: {
    passProj() {
      var that = this;

      api.review_project(that.id).then(function(e) {
        if (e["data"]["code"] == "200") {
          that.$message("操作成功!");
          that.$router.push("/ContestList");
        } else if (e["data"]["code"] != "200") {
          that.$message("操作异常!");
        }
      });
    },
    backProj() {
      var that = this;

      api.revert_project(that.id).then(function(e) {
        if (e["data"]["code"] == "200") {
          that.$message("退回成功!");
          that.$router.push("/ContestList");
        } else if (e["data"]["code"] != "200") {
          that.$message("操作异常!");
        }
      });
    }
  },
  created() {
    this.id = this.$route.query.id;
    var that = this;
    api.administrator_get_project(this.id).then(function(e) {
      var res = JSON.parse(e.data.data);
      that.state = res["state"];
      if (res["state"] == 1) {
        that.projectState = false;
      } else {
        that.projectState = true;
      }
      var relation = Object.keys(res["expert_info"]);
      for (var i = 0; i < relation.length; i++) {
        that.expTags.push(
          {
            relation_id: relation[i],
            name: res["expert_info"][relation[i]][1],
            id: res["expert_info"][relation[i]][0]
          }
        );
      }
    });
  }
};
</script>
<style scoped>
.applyInfoForm {
  width: 75%;
}
</style>

