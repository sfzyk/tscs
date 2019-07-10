<template>
  <div style="width: 100%;">
    <el-row style="margin-top: 10px;">
      <el-col :span="4" style="text-align: right;">
        报名截止时间：
      </el-col>
      <el-col :span="8" style="text-align: left;">
        {{dateFormat(Info.checkin_expire_date)}}
      </el-col>
      <el-col :span="4" style="text-align: right;">
        初评截止时间：
      </el-col>
      <el-col :span="8" style="text-align: left;">
        {{dateFormat(Info.expire_date)}}
      </el-col>
    </el-row>
    <el-row style="margin-top:20px; height: 120px;">
      <el-input class="info" v-model="Info.descriptions" type="textarea" :autosize="{ minRows: 8, maxRows: 10}" disabled></el-input>
    </el-row>
    <div style="width:100%; margin-top: 25px;">
      <el-steps :active="Info.state" simple finish-status="success">
        <el-step title="创建"></el-step>
        <el-step title="报名"></el-step>
        <el-step title="初审"></el-step>
        <el-step title="初评"></el-step>
        <el-step title="筛选"></el-step>
        <el-step title="最终答辩"></el-step>
      </el-steps>
    </div>

  </div>
</template>

<script>
  import api from "@/api/apis";
    export default {
      name: "ContestInfoHead",
      props:{
        contest_id:{
          type:Number,
          required:true,
        }
      },
      data:function(){
        return{
          Info:{},
        }
      },
      created:function(){
        var that=this;
        api.get_contest_info(this.contest_id).then(
          function(res){
            that.Info=eval('('+res['data']['data']['contest_info']+')');
            that.$emit('HeadFinish');
          }
        );
      },
      methods:{
        dateFormat:function(time) {
          var date=new Date(time);
          var year=date.getFullYear();
          var month= date.getMonth()+1<10 ? "0"+(date.getMonth()+1) : date.getMonth()+1;
          var day=date.getDate()<10 ? "0"+date.getDate() : date.getDate();
          var hours=date.getHours()<10 ? "0"+date.getHours() : date.getHours();
          var minutes=date.getMinutes()<10 ? "0"+date.getMinutes() : date.getMinutes();
          var seconds=date.getSeconds()<10 ? "0"+date.getSeconds() : date.getSeconds();
          // 拼接
          return year+"年 "+month+"月 "+day+"日";
        },
        initInfo(){
          var that=this;
          api.get_contest_info(this.contest_id).then(
            function(res){
              that.Info=eval('('+res['data']['data']['contest_info']+')');
            }
          );
        }
      }
    }
</script>

<style scoped>
  .info {
    font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", 微软雅黑;
    font-size: 16px;
    margin-top: 5px;
    margin-bottom: 10px;
    float:left;
    color: #333;
  }
</style>
