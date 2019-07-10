<template>
    <div class="bodycontainer">
      <el-card>
        <div slot="header" >
          <span class="title">{{Info.name}}</span>
        </div>
        <el-row style="margin-top: 10px;">
          <el-col :span="4" style="text-align: right;">
            报名截止时间：
          </el-col>
          <el-col :span="8" style="text-align: left;">
            {{dateFormat(Info.checkin_expire_date)}}
          </el-col>
          <el-col :span="4" style="text-align: right;">
            结束时间：
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
        <div>
          <ConProjectList
            :prolist="prolist"
            :Spagesize="pagesize"
            :pagetotal="total"
            @pagechange="show"
            type=1
            @search="search"
            ref="projects"
          ></ConProjectList>
        </div>
      </el-card>
    </div>
</template>

<script>
  import ConProjectList from "@/components/ConProjectList.vue"
  import api from "@/api/apis";
    export default {
      name: "ContestInfo",
      components:{
          ConProjectList
        },
      data:function(){
          return{
            contest_id:0,
            contest_info:{},
            prolist:[{}],
            pagesize: 8,
            total: 0,
            Info:{},
        }
      },
      created:function(){
        this.contest_id = this.$route.query.id;
        this.contest_info=this.GetInfo(this.contest_id);
        var that=this;
        api.get_contest_info(this.contest_id).then(
          function(res){
            that.Info=eval('('+res['data']['data']['contest_info']+')');
          }
        );
        api.admin_get_projects(0, this.pagesize,this.contest_info).then(function(result) {
          // console.log(result);
          // console.log(result["data"]["data"]["data"]);
          console.log(5555)
          console.log(result);
          that.prolist = result["data"]["data"]["data"];
          var l = that.prolist.length;
          if (l % that.pagesize != 0) {
            for (var i = 0; i < that.pagesize - (l % that.pagesize); i++) {
              that.prolist.push({ id: 0 });
            }
          }
          that.total = result["data"]["data"]["num"];
        });
      },
      methods:{
        GetInfo(Cid){
          var sea={'contest_id':Cid};
          var info={'field':'id','order':'1','search':JSON.stringify(sea)};
          return info;
        },
        search(searchword){
          console.log(searchword)
        },
        show(val) {
          var that = this;
          //console.log(val);
          api.admin_get_projects(val - 1, this.pagesize,this.contest_info).then(function(result) {
            //console.log(result);
            //console.log(result["data"]["data"]["data"]);
            that.prolist = result["data"]["data"]["data"];
            var l = that.prolist.length;
            if (l % that.pagesize != 0) {
              for (var i = 0; i < that.pagesize - (l % that.pagesize); i++) {
                that.prolist.push({ id: 0 });
              }
            }
            that.total = result["data"]["data"]["num"];
            console.log(that.prolist);
          });
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
      }
    }
</script>

<style scoped>
  .bodycontainer{
    margin: 0px 145px 20px 145px;
    height: 100%;
  }
  .bodyhead{
    background-color:#BEE;
    width:800px;
  }
  .title {
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", 微软雅黑;
  font-size: 28px;
  font-weight: 400;
  margin-bottom: 6px;
  float:none;
  color: #06c;
}
.info {
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", 微软雅黑;
  font-size: 16px;
  margin-top: 5px;
  margin-bottom: 10px;
  float:left;
  color: #333;
}
</style>
