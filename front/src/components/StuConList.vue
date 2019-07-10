<template>
  <div class="bodycontainer">
    <el-tabs type="border-card" tab-position="left" style="height: 100%;">
      <el-tab-pane label="全部">
        <ContestItem
          v-for="Contest in ContestList"
          :key="Contest.id"
          :Cid='Contest.id'
          :Ctype='Contest.state'
          :name="Contest.name"
          :checkin_end="dateFormat(Contest.checkin_expire_date)"
          :end="dateFormat(Contest.expire_date)"
          :description="Contest.descriptions"
          :priority="priority"
          @DelEvent="Delinit()">
        </ContestItem>
        <div class="Pager">
          <el-pagination
            background
            layout="jumper,prev, pager, next"
            :page-size="PageSize"
            :page-count="ContestPage"
            :current-page="CurrentPage"
            :pager-count="5"
            @current-change="handleCurrentChange">
          </el-pagination>
        </div>
      </el-tab-pane>
      <el-tab-pane label="报名">
        <ContestCategory :category="GetInfo(1)" :priority="priority"></ContestCategory>
      </el-tab-pane>
      <el-tab-pane label="答辩名单">
        <ContestCategory :category="GetInfo(5)" :priority="priority"></ContestCategory>
      </el-tab-pane>
      <el-tab-pane label="最终名单">
        <ContestCategory :category="GetInfo(6)" :priority="priority"></ContestCategory>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import ContestItem from './ContestItem.vue';
  import api from '@/api/apis.js';
  import router from "@/router";
  import ContestCategory from './ContestCategory.vue';
    export default {
      name: "StuConList",
      components:{
        ContestItem,
        ContestCategory,
      },
      data:function(){
        return {
          ContestList:[],
          ContestPage:0,
          PageSize:3,
          CurrentPage:1,
          priority:0
        }
      },
      created:function(){
        this.GetData();
      },
      methods:{
        GetInfo(Cnum){
          var search={};
          search['state']=Cnum;
          var info={'field':'id','order':'1','search':JSON.stringify(search)};
          return info;
        },
        AddJump(){
          router.push('/contestRegister');
        },
        GetData(){
          var that=this;
          api.student_get_contest(that.CurrentPage-1,that.PageSize,{'field':'id','order':'1','search':JSON.stringify("{}")}).then(
            function(res){
              console.log(res);
              that.ContestPage=res['data']['data']['num'];
              var temp=res['data']['data']['data'];
              for(var i=0;i<temp.length;i++)
              {
                that.ContestList.push(eval('('+temp[i]+')'));
              }
              if(temp.length<3)
              {
                for(var j=1;j<=3-temp.length;j++)
                {
                  var tempj={
                    'id':that.ContestPage*that.PageSize+j,
                    'state':-1,
                    'name':'',
                    'expire_date':'',
                    'checkin_expire_date':''
                  };
                  that.ContestList.push(tempj);
                }
              }
            }
          )
        },
        handleCurrentChange(currentPage){
          this.ContestList=[];
          this.CurrentPage=currentPage;
          this.GetData();
        },
        Delinit:function(){
          this.ContestList=[];
          var that=this;
          api.student_get_contest(that.CurrentPage-1,that.PageSize,{'field':'id','order':'1','search':JSON.stringify("{}")}).then(
            function(res){
              console.log(res);
              var num=res['data']['data']['num'];
              var PageNum=num;
              if(that.CurrentPage>PageNum)
              {
                that.CurrentPage=PageNum;
                that.GetData();
              }
              else
              {
                that.ContestPage=res['data']['data']['num'];
                var temp=res['data']['data']['data'];
                for(var i=0;i<temp.length;i++)
                {
                  that.ContestList.push(eval('('+temp[i]+')'));
                }
                if(temp.length<3)
                {
                  for(var j=1;j<=3-temp.length;j++)
                  {
                    var tempj={
                      'id':that.ContestPage*that.PageSize+j,
                      'state':-1,
                      'name':'',
                      'expire_date':'',
                      'checkin_expire_date':''
                    };
                    that.ContestList.push(tempj);
                  }
                }
              }
            }
          )
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
    height: 820px;
  }
  /deep/.el-tabs__item{
    height: 60px;
    font-size: 16px;
    line-height: 60px;
    width:150px;
  }
  /deep/.el-tabs--left .el-tabs__item.is-left{
    text-align: center;
  }
  .Pager{
    height: 50px;
    margin-top: auto;
    margin-bottom: 0px;
    width: 100%;
  }
  .AddTop{
    height:2%;
    width: 100%;
  }
</style>
