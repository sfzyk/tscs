<template>
<el-container class='body' align="center" style="note"> 
  <el-main>
    <el-card class="box" v-model="sentense" style="margin-top:5%">
            <div class="text item" text-size="30">
                {{ sentense }}
        </div>
    </el-card>
  </el-main>
  <el-footer>
    <el-row>
      <el-col :span="10" :offset="2">
       <el-button type="success" @click="isagree()" v-show="agree">同意评审</el-button>
      </el-col>
      <el-col :span="10">
       <el-button type="danger" @click="refuse()" v-show="agree">拒绝评审</el-button>
      </el-col>
    </el-row>
    </el-footer>
</el-container>

</template>
<script>
import api from '@/api/apis'

export default {
  name:"invitation",
    data(){
      return {
        id:"",
        agree:true,
        sentense:"尊敬的老师您好：现特邀请您参加科技项目竞赛评审工作，请问您时间是否允许。    校团委",
        note: {
          backgroundImage: "url(" + require("@/assets/p6.jpg") + ")",
          backgroundRepeat: "no-repeat"
        },
      }
    },
    created: function(){
      this.id=this.$route.path;
      this.id = (this.$route.path.split("/"))[2]
      console.log(this.id);
    },
    methods:{
        isagree() {
            //console.log('hh')
        
            this.$router.push({path:'/resetpasswd',query:{id:this.id}})
        },
        refuse(){
          this.agree=false
          this.sentense="您已拒绝，感谢您的时间"
          api.invitation_reset({
             uni_link:that.id,
             join:1
          })
          //this.$message("您已拒绝")
        }
    }
}
</script>


<style scoped>
  .body{
      background-color: whitesmoke;
      width:40%;
      height:30%;
      margin: 150px auto 150px auto;
  }
  .el-header, .el-footer {
    background-color:  #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  .box{
    opacity: 0.9;
  }
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    /* text-align: center; */
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    /* text-align: center; */
    /* line-height: 160px; */
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
