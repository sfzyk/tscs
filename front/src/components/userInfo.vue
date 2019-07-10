<template>
  <div class="bodycontainer">
    <el-card style="height: 100%;">
        <div style="width: 95%; height: 60px;font-size: 20px; text-align: left; margin-left: 5%;margin-top: 20px;">
          {{tab1}}
        </div>
        <div class="rightbody">
          <el-row :gutter="20" style="margin-top: 10%;">
            <el-col :span="6"><div class="linehead">姓名:</div></el-col>
            <el-col :span="18"><div class="linebody"><modifybox v-on:update="initdata()" name="name" :content="name"></modifybox></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
            <el-col :span="6"><div class="linehead">学号:</div></el-col>
            <el-col :span="18"><div class="linebody"><div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{student_id}}</div></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
          <el-col :span="6"><div class="linehead">专业:</div></el-col>
          <el-col :span="18"><div class="linebody"><modifybox v-on:update="initdata()" name="major" :content="major"></modifybox></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
            <el-col :span="6"><div class="linehead">电话:</div></el-col>
            <el-col :span="18"><div class="linebody"><modifybox v-on:update="initdata()" Rtype="tel" name="telephone" :content="telephone"></modifybox></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
            <el-col :span="6"><div class="linehead">邮箱:</div></el-col>
            <el-col :span="18"><div class="linebody"><div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{email}}</div></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
            <el-col :span="6"><div class="linehead">部门:</div></el-col>
            <el-col :span="18"><div class="linebody"><modifybox v-on:update="initdata()" name="department" :content="department"></modifybox></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
            <el-col :span="6"><div class="linehead">年份:</div></el-col>
            <el-col :span="18"><div class="linebody"><modifybox v-on:update="initdata()" Rtype="year" name="year" :content="year"></modifybox></div></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 5%;">
            <el-col :span="6"><div class="linehead">生日:</div></el-col>
            <el-col :span="18"><div class="linebody"><el-date-picker v-model="birth_dateB" format="yyyy年 MM月 dd日" :clearable="clear" type="date" :picker-options="pickerOptions" @change="datechange()"></el-date-picker></div></el-col>
          </el-row><!--用相应的输入来代替原本的输入框-->
        </div>
    </el-card>
  </div>
</template>

<script>
  import modifybox from "./modifybox.vue";
  import api from "@/api/apis";

    export default {
      name: "userInfo",
      components: {
        modifybox,
      },
      data:function() {
          return {
            tab1:"个人信息",
            tab2:"获奖记录",
            clear:false,
            id:0,
            student_id:'',
            name:'',
            major:'',
            telephone:'',
            year:0,
            email:'',
            department: '',
            birth_date: '',
            birth_dateB:'',
            pickerOptions: {
              disabledDate(time) {
                return time.getTime() > Date.now();
              },
            },
          };
        },
      created:function(){
        this.initdata();
      },
      watch:{
        birth_date:function () {
          this.birth_dateB=this.birth_date;
        }
      },
      methods:{
        initdata:function(){
          var that=this;
          api.get_user_info().then(
            function (res) {
              console.log(res);
              that.id=res['data']['data']['id'];
              that.student_id=res['data']['data']['student_id'];
              that.name=res['data']['data']['name'];
              that.major=res['data']['data']['major'];
              that.telephone=res['data']['data']['telephone'];
              that.year=res['data']['data']['year'];
              that.email=res['data']['data']['email'];
              that.department=res['data']['data']['department'];
              that.birth_date=res['data']['data']['birth_date'];
            }
          );
          this.birth_date=this.dateFormat(this.birth_date);
        },
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
        datechange:function(){
          if(this.birth_dateB=="")
          {
            this.$message({
              message: '不可为空',
              type:'error',
              center:true
            });
            this.birth_dateB=this.birth_date;
          }
          else if(this.birth_dateB==this.birth_date)
          {
          }
          else
          {
            var info={'birth_date':this.birth_dateB};
            var that=this;
            api.modify_user_info(info).then(
              function (e) {
                console.log(e);
                if(e['data']['code']==200)
                {
                  that.$message({
                    message: '已提交',
                    type:'success',
                    center:true
                  });
                }
                else
                {
                  that.$message({
                    message: '抱歉，服务器出问题了，请稍后重试',
                  });
                }
              }
            );
            this.initdata();
          }
        },
      }
    }
</script>

<style scoped>
  .bodycontainer{
    margin: 0px 145px 20px 145px;
    height: 800px;
  }
  /deep/.el-tabs__header{
    width: 200px;
  }
  /deep/.el-tabs__nav{
    margin-top: 80px;
  }
  /deep/.el-tabs__item{
    height: 60px;
    font-size: 18px;
    text-align: center;
    line-height: 60px;
  }
  /deep/.el-tabs--left .el-tabs__item.is-left{
    text-align: center;
  }
  /deep/.el-tabs__content{
    text-align: center;
  }
  .linehead{
    height: 40px;
    width: 100%;
    text-align: center;
    line-height: 40px;
    text-align: left;
  }
  .linebody{
    height: 40px;
    width: 100%;
    text-align: left;
  }
  .rightbody{
    width: 600px;
    margin: 30px auto;
  }
  .rightbody2{
    margin: 30px 0px;
  }
</style>
