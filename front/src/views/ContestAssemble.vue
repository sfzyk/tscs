<template>
  <div class="bodycontainer">
    <el-card>
      <div slot="header" >
        <span class="title">{{Head}}</span>
      </div>
      <div>
      <ContestInfoHead :contest_id="contest_id" ref="CHead" @HeadFinish="GetHead"></ContestInfoHead>
      </div>
      <div v-if="priority==0">
        <div v-if="state==1">
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
          <div style="height:100px; width:100%; background-color:white; opacity:0.6">
            <el-button type="primary" round icon="el-icon-circle-plus-outline" @click="addproject">添加项目</el-button>
          </div>
        </div>
        <div v-if="state==2">
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==3">
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==4">
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==5">
<!--          应该是答辩名单-->
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==6">
<!--          应该是最终结果名单-->
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
      </div>
      <div v-if="priority==2">
        <!--<div>
          <el-row style="height:50px; margin-top: 20px;">
            <el-col :span="4" style="text-align: right">
              暂存中:
            </el-col>
            <el-col :span="4" style="text-align: center">
              {{ProItem[1]}}
            </el-col>
            <el-col :span="4" style="text-align: right">
              等待初审:
            </el-col>
            <el-col :span="4" style="text-align: center">
              {{ProItem[2]}}
            </el-col>
            <el-col :span="4" style="text-align: right">
              等待专家评审:
            </el-col>
            <el-col :span="4" style="text-align: center">
              {{ProItem[3]}}
            </el-col>
          </el-row>
          <el-row style="height:50px;">
            <el-col :span="4" style="text-align: right">
              专家评审通过:
            </el-col>
            <el-col :span="4" style="text-align: center">
              {{ProItem[4]}}
            </el-col>
            <el-col :span="4" style="text-align: right">
              进入答辩名单:
            </el-col>
            <el-col :span="4" style="text-align: center">
              {{ProItem[5]}}
            </el-col>
            <el-col :span="4" style="text-align: right">
              已有最终结果:
            </el-col>
            <el-col :span="4" style="text-align: center">
              {{ProItem[6]}}
            </el-col>
          </el-row>
        </div>-->
        <div v-if="state==0">
          <!--创建-->
          <el-button type="primary" round @click="Publish()">发布比赛</el-button>
        </div>
        <div v-if="state==1">
          <div style="margin: 20px auto;">
            报名完成情况：<el-progress :percentage="normalize((ProItem[2]/(ProItem[1]+ProItem[2])*100).toFixed(1))"></el-progress>
          </div>
          <el-row>
            <el-col>
              <el-button type="primary" round @click="stop_checkin()">截止报名</el-button>
            </el-col>
          </el-row>
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==2">
          <div style="margin: 20px auto;">
            初审完成情况：<el-progress :percentage="normalize((ProItem[3]/(ProItem[2]+ProItem[3])*100).toFixed(1))"></el-progress>
          </div>
          <el-row>
            <el-button type="success" round @click="Finish2()">完成初审</el-button>
          </el-row>
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==3">
          <div style="margin: 20px auto;">
            初评完成情况<el-progress :percentage="normalize((ProItem[4]/(ProItem[3]+ProItem[4])*100).toFixed(1))"></el-progress>
          </div>
          <el-row>
            <el-col :span="24">
              <el-button type="success" round @click="Finish3()">完成初评</el-button>
            </el-col>
          </el-row>
          <admin-expertlist @dispatch_change="getPer()" :contestid="contest_id"></admin-expertlist>
          <div style="width: 100%; height: 100px;margin-top: 20px;">
            <el-row>
              <el-col :span="12">
                <el-button type="primary" round @click="autoExpert()">自动分配</el-button>
              </el-col>
              <el-col :span="12">
                <el-button type="danger" round @click="resetExpert()">重置分配</el-button>
              </el-col>
            </el-row>
            <el-row style="margin: 20px auto;" :gutter="20">
              <el-col :span="6">
                <el-row>
                  <el-col :span="24">
                    分配情况
                  </el-col>
                </el-row>
                <el-row style="margin-top:10px;">
                  <el-col :span="24">
                    <el-progress :percentage="dispatch_per" type="circle"></el-progress>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="6">
                <el-row>
                  <el-col :span="24">
                    邀请情况
                  </el-col>
                </el-row>
                <el-row style="margin-top:10px;">
                  <el-col :span="24">
                    <el-progress :percentage="invite_per" type="circle"></el-progress>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="12">
                <el-row style="margin-top: 20px;">
                  <el-col :span="12" style="text-align: right;">
                    未响应邀请的人数：
                  </el-col>
                  <el-col :span="12">
                    {{invite_num[1]}}
                  </el-col>
                </el-row>
                <el-row style="margin-top: 20px;">
                  <el-col :span="12" style="text-align: right;">
                    同意的人数：
                  </el-col>
                  <el-col :span="12">
                    {{invite_num[2]}}
                  </el-col>
                </el-row>
                <el-row style="margin-top: 20px;">
                  <el-col :span="12" style="text-align: right;">
                    拒绝人数：
                  </el-col>
                  <el-col :span="12">
                    {{invite_num[3]}}
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-button type="success" round @click="Invite()">向专家发送邀请</el-button>
              </el-col>
            </el-row>
          </div>
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==4">
          <!--筛选-->
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==5">
          <!--最终发布-->
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
        <div v-if="state==6">
          <!--显示最终发布的比赛结果-->
          <ConProTotal :contest_id="contest_id" :priority="priority"></ConProTotal>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
  import ContestInfoHead from '@/components/ContestInfoHead.vue';
  import ConProTotal from "@/components/ConProTotal.vue"
  import ContestOncreate from '@/components/ContestOnCreate.vue'
  import api from "@/api/apis";
  import router from '@/router.js';
  import adminExpertlist from '@/components/adminExpertlist.vue';
    export default {
      name: "ContestAssemble",
      components:{
        ConProTotal,
        ContestInfoHead,
        //ContestOncreate,
        adminExpertlist,
      },
      data:function(){
        return{
          contest_id:0,
          state:0,
          Head:'',
          ProItem:[],
          priority:0,
          dispatch_per:0,
          invite_per:0,
          invite_num:[]
        }
      },
      created:function(){
        this.contest_id = this.$route.query.id;
        this.priority=this.$route.query.priority;
        var that=this;
        api.get_contest_info(this.contest_id).then(
          function(res){
            var info=eval('('+res['data']['data']['contest_info']+')');
            that.state=info.state;
            that.ProItem=res['data']['data']['detail_info'];
            if(that.state==3)
            {
              that.getPer();
            }
          }
        );
      },
      methods:{
        initdata(){
          var that=this;
          api.get_contest_info(this.contest_id).then(
            function(res){
              var info=eval('('+res['data']['data']['contest_info']+')');
              that.state=info.state;
              that.ProItem=res['data']['data']['detail_info'];
              if(that.state==3)
              {
                that.getPer();
              }
              that.$refs.CHead.initInfo();
            }
          );
        },
        getPer(){
          var that=this;
          api.dispatch_percent(this.contest_id).then(
            function(res){
              var temp=res['data']['data'];
              that.dispatch_per=temp[0];
              that.invite_per=that.normalize(temp[2]/(temp[1]+temp[2]+temp[3])*100);
              that.invite_num=temp;
            }
          )
        },
        GetHead(){
          this.Head=this.$refs.CHead.Info.name;
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
        Publish(){
          var that=this;
          api.publish_contest(this.contest_id).then(
            function(res){
              if(res['data']['code']==200)
              {
                that.$message({
                  message:'发布成功',
                  type:'success',
                  center:true,
                });
                that.initdata();
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
        Finish2(){
          var that=this;
          api.get_contest_info(this.contest_id).then(
            function(res){
              // 0  全部
              // 1  "暂存中",
              // 2  "等待初审",
              // 3  "初审通过等待专家评审",
              // 4  "专家评审通过",
              // 5  "进入答辩名单",
              // 6  "已有最终结果"
              var temp=res['data']['data']['detail_info'];//eval('('+res['data']['data']['contest_info']+')');
              if(temp[2]>0)
              {
                that.$message({
                  message: '请完成审核',
                  type: 'error',
                  center:true
                });
              }
              else
              {
                that.changeState2();
                that.$message({
                  type: 'success',
                  message: '完成初审',
                  center:true
                });
              }
            }
          );
        },
        Finish3(){
          var that=this;
          api.get_contest_info(this.contest_id).then(
            function(res){
              var temp=res['data']['data']['detail_info'];//eval('('+res['data']['data']['contest_info']+')');
              if(temp[3]>0)
              {
                that.$message({
                  message: '专家还未完成所有作品的评审',
                  type: 'error',
                });
              }
              else
              {
                that.changeState3();
                that.$message({
                  type: 'success',
                  message: '完成初评',
                  center:true
                });
                router.push({
                  path:'/FinalSelect',
                  query:{
                    contest_id:that.contest_id
                  }
                })
              }
            }
          );
        },
        changeState2(){
          var that =this
          api.finish_check_contest(this.contest_id).then(function(){that.initdata();});
        },
        changeState3(){
          var that =this
          api.recheck_contest(this.contest_id).then(function(){that.initdata();});
        },
        addproject() {
          var that = this;
          api
            .stage_application(
              "{}",// cooperatorinfo,
              "", //email,
              "未命名项目",//fullname,
              "",//telephone,
              "", //address,
              "", //innovation
              "", //keywords,
              "0", //category,
              "", //descriptions
              "0",// education_background,
              "0",//,type,
              "['0']",//type_info
              this.contest_id,//contest_id
            )
            .then(function(result) {
              var pid = result["data"]['data'];
              that.$router.push({
                path: "/stuApplyInfo",
                query: {
                  id: pid
                }
              });
            });
          //this.$router.push('/applyInfo')
        },
        autoExpert(){
          var that =this 
          api.auto_dispatch(this.contest_id).then(
            function(){
              that.getPer();
            }
            
          );
        },
        resetExpert(){
          var that =this
          api.reset_dispatch(this.contest_id).then(
            function(){
              that.getPer();
            }
          )
        },
        Invite(){
          var that=this;
          api.send_email(this.contest_id).then(
            function(error){
              var temp=error['data']['data'];
              if(temp>0)
              {
                that.$message({
                  message:'有'+temp.toString()+'个邀请发送失败',
                  type:'warning',
                  center:true
                })
              }
              else
              {
                that.$message({
                  message:'发送成功',
                  type:'success',
                  center:true
                })
              }
              that.getPer();
            }
          )
        },
        stop_checkin(){
          var that=this;
          api.stop_checkin_contest(this.contest_id).then(function(){
            that.initdata();
          });
          
        },
        normalize(k){
          if(isNaN(k))
          {
            return 0;
          }
          else
          {
            return k;
          }
        }
      }
    }
</script>

<style scoped>
  .bodycontainer{
    margin: 0px 145px 20px 145px;
    height: 100%;
  }
  .title {
    font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", 微软雅黑;
    font-size: 28px;
    font-weight: 400;
    margin-bottom: 6px;
    float:none;
    color: #06c;
  }
</style>
