<template>
  <div style="height:100%">
    <el-container class="body">
      <el-card class="box-card">
        <div class="text-title">{{title}}</div>
        <div class="text-time" style="margin-top:10px">{{time}}</div>
        <div class="text-content" style="margin-top:20px">{{content}}</div>
      </el-card>
    </el-container>
    <div style="margin-top:20px">
      <el-button type="primary" v-if="isattach" @click="download()">下载附件</el-button>
    </div>
  </div>
</template>

<script>
import api from "@/api/apis"
export default {
  data() {
    return {
      id:"",
      title: "标题",
      time: "2019-1-1",
      content: "哈哈哈哈哈",
      isattach:true,
    };
  },
  created:function(){
      var that = this;
      this.id=this.$route.query.id;
      api.get_notice(this.id).then(function(e){
          var res = e["data"]["data"];
          console.log("hahahah"+res["attach"])
          that.title = res["title"];
          that.time = res["time"];
          that.content = res["content"];
          console.log("attach:"+res["attach"]);
          if(res["attach"]===undefined){
              that.isattach=false;
          }
      })
  },
  methods:{
      download(){
          this.id=this.$route.query.id;
          api.get_attach(this.id).then(function(e){

          })
      }
  }
};
</script>

<style scoped>
.body {
  height: 64%;
  width: 70%;
  margin: 40px auto 0 auto;
}
.box-card {
  margin: 0 auto 0 auto;
  height: 100%;
  width: 90%;
}
.text-title{
    font-size:30px;
}
.text-time{
    font-size:12px;
}
</style>
