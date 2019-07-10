<template>
  <div>
    <div v-for="item in comment" :key="item" style="margin:10px auto ">
      <el-row>
        <el-col :span="3" style="margin:auto;height:100%">{{item.expert_name}}</el-col>
        <el-col :span="3" style="margin:auto;height:100%">打分：{{item.score}}</el-col>
        <el-col :span="18"><el-input type="textarea" v-model="item.comment" disabled></el-input></el-col>
      </el-row>
      
    </div>
  </div>
</template>
<script>
import api from "@/api/apis";
export default {
  props: { proId: String },
  data() {
    return {
      comment: []
    };
  },
  created() {
    var that = this;
    api.admin_commmet(that.proId).then(function(res){
      console.log(res)
      for(var i = 0 ; i<res['data']['data'].length;i++)
      {
        that.comment.push(JSON.parse(res['data']['data'][i]))
      }
    });
  }
};
</script>

