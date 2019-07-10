<template>
  <el-card class="applyInfoForm" shadow="always" style="margin: 0 auto;">
    <ApplyInfo ref="applyinfo" :id="id" role="expert"></ApplyInfo>
    <el-form label-position="right" label-width="80px" style="width:100%" :inline="true" :model="form" ref="form">
      <el-form-item label="作品评价" prop="evaluation" :rules="{
              required: true, message: '评价不能为空', trigger: 'blur'
            }">
        <el-input v-model="form.evaluation" class="Input" type="textarea" :autosize="{minRows:3,maxRows:10}" :disabled="limit"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="作品评分" prop="value" :rules="{
              required: true, message: '评分不能为空', trigger: 'blur'
            }">
        <el-row>
          <el-col :span="10" :offset="4">
            <el-rate v-model="form.value" show-score text-color="#ff9900" :colors="colors" :low-threshold="3"
              :high-threshold="8" score-template="{value}" class="Input" :max="10" allow-half align="left"
              style="margin: 10px auto 0 0;" :disabled="limit"></el-rate>
          </el-col>
        </el-row>

      </el-form-item>
      <br />
      <el-button @click="stageEvaluation('form')" :disabled="limit">保存</el-button>
      <el-button @click="submitEvaluation('form')" :disabled="limit">提交</el-button>
    </el-form>
  </el-card>
</template>

<script>
// @ is an alias to /src
import ApplyInfo from "@/components/ApplyInfo.vue";
import api from "@/api/apis";

export default {
  name: "expertApplyInfo",
  components: {
    ApplyInfo
  },
  data() {
    return {
      limit : true,
      form: {
        value: 5.0,
        evaluation: ""
      },
      colors: ["#99A9BF", "#F7BA2A", "#FF9900"]
    };
  },
  methods: {
    submitEvaluation(formName) {
      var that = this;
      this.$refs[formName].validate(valid => {
        if (valid) {
            that.save(function(res) {
              console.log(res)
              if (res["data"]["code"] == 200) {
                api.commit_comment(that.id).then(function(res) {
                  console.log(res)
                  if (res["data"]["code"] == 200) {
                    
                    that.$message("submit!");
                    that.$router.push("/Expproject");
                  }
                  else that.$message("error submit!");
                });
              }
            });
        } else {
          that.$message("提交失败，请填写完整");
          return false;
        }
      });
    },
    stageEvaluation(){
      var that = this;
      that.save(function(res) {
        if (res["data"]["code"] == 200) {
          that.$message("保存成功");
          that.$router.push("/Expproject");
        } else {
          that.$message("保存失败");
        }
      });
    },
    save(func) {
      var that = this;
      api
        .stage_comment(that.id, that.form.evaluation, that.form.value)
        .then(func);
    }
  },
  created() {
    this.id = this.$route.query.id;
    var that = this
    api.get_expert_project_comment(that.id).then(function(e) {
      console.log(e)
      that.form.value = e['data']['data']['score']
      that.form.evaluation = e['data']['data']['comment']
      if(e['data']['data']['state'] == 1){
        that.limit = true
      }
      else {
        that.limit =false
      }
      
    })
  }
};
</script>
<style scoped>
.applyInfoForm {
  width: 75%;
}
.Input {
  width: 500px;
}
</style>
