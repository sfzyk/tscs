<template>
  <el-row>
    <el-button type="primary" round @click="Publish()">发布比赛</el-button>
    <!--<el-button type="info" round>修改比赛</el-button>
    <el-button type="danger" round>删除比赛</el-button>-->
  </el-row>
</template>

<script>
  import api from '@/api/apis.js';
  import router from "@/router";

    export default {
      name: "ContestOnCreate",
      props:{
        contest_id:{
          type:Number,
          required:true,
        }
      },
      methods:{
        Publish(){
          var that=this;
          api.publish_contest(this.contest_id).then(
            function(res){
              console.log(555);
              console.log(res);
              if(res['data']['code']==200)
              {
                that.$message({
                  message:'发布成功',
                  type:'success',
                  center:true,
                });
                router.push('/ContestList');
              }
              else{
                that.$message({
                  message:'发布失败，稍后重试',
                  type:'error'
                });
              }
            }
          );
        },
      },
    }
</script>

<style scoped>

</style>
