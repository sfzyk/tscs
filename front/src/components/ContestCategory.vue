<template>
  <div style="width:100%;height:98%;">
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
  </div>
</template>

<script>
  import ContestItem from './ContestItem.vue';
  import api from '@/api/apis.js';

    export default {
      name: "ContestCategory",
      components:{
        ContestItem,
      },
      props:{
        category:{},
        priority:{
          type:Number,
          required:true
        }
      },
      data:function(){
        return {
          ContestList:[],
          ContestPage:0,
          PageSize:3,
          CurrentPage:1,
        }
      },
      created:function(){
        this.GetData();
      },
      methods:{
        GetData(){
          var that=this;
          if(this.priority==2)
          {
            api.get_contest(that.CurrentPage-1,that.PageSize,that.category).then(
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
            );
          }
          else if(this.priority==0)
          {
            api.student_get_contest(that.CurrentPage-1,that.PageSize,that.category).then(
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
            );
          }
          else
          {
            alert('专家的');
          }
        },
        handleCurrentChange(currentPage){
          this.ContestList=[];
          this.CurrentPage=currentPage;
          this.GetData();
        },
        Delinit:function(){
          this.ContestList=[];
          var that=this;
          if(this.priority==2)
          {
            api.get_contest(that.CurrentPage-1,that.PageSize,that.category).then(
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
            );
          }
          else if(this.priority==0)
          {
            api.student_get_contest(that.CurrentPage-1,that.PageSize,that.category).then(
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
            );
          }
          else
          {
            alert('专家的')
          }
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
  .Pager{
    height: 50px;
    margin-top: auto;
    margin-bottom: 0px;
    width: 100%;
  }
</style>
