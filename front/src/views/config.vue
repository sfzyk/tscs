<template>
  <el-card style="width:75%;margin:40px auto;">
    <el-row style="margin: 30px">
      <el-col :span="6" :offset="4">
        <div style="width:100%;height:100%;margin: 10px auto;">每个项目专家人数：</div>
      </el-col>
      <el-col :span="8">
        <el-input v-model="input1" type="number"></el-input>
      </el-col>
    </el-row>
    <el-row style="margin: 30px">
      <el-col :span="6" :offset="4">
        <div style="width:100%;height:100%;margin: 10px auto;">每个比赛默认答辩人数：</div>
      </el-col>
      <el-col :span="8">
        <el-input v-model="input2" type="number"></el-input>
      </el-col>
    </el-row>
    <el-row style="margin: 30px">
      <el-col :span="12" offset="4">
        <el-button type="primary" icon="el-icon-edit" round @click="submit">提交</el-button>
      </el-col>
    </el-row>
  </el-card>
</template>
<script>
import api from "@/api/apis";
export default {
  name: "config",
  data() {
    return {
      input1: "",
      input2: ""
    };
  },
  methods: {
    submit() {
      var that = this;
      api
        .modifty({
          expert_per_proj: this.input1,
          num_proj: this.input2
        })
        .then(function(result) {
          if(result['data']['code']==200)
          {
              that.$message({
              message: "上传成功！",
              type: "success"
            });
          }
          else {
              that.$message.error("修改出现错误！");
          }
        });
    }
  },
  created() {
    var that = this;
    api.get_info().then(function(result) {
      that.input1 = result["data"]["data"]["expert_per_proj"];
      that.input2 = result["data"]["data"]["num_proj"];
    });
  }
};
</script>
