<template>
  <div style="width: 100%;height: 100%">
    <el-row class="mod-row" v-if="!checked">
      <el-col :span="22" class="mod-col">
        <div id="wenben">{{contentB}}</div>
      </el-col>
      <el-col :span="2" class="mod-col" style="line-height: 40px;">
        <i class="el-icon-edit" @click="change()"></i>
      </el-col>
    </el-row>
    <el-row class="mod-row" v-if="checked">
      <el-col :span="22" class="mod-col">
        <el-input v-model="contentB"></el-input>
      </el-col>
      <el-col :span="2" class="mod-col" style="line-height: 40px;">
        <i class="el-icon-check" @click="submit()"></i>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import api from "@/api/apis";
export default {
  name: 'modifybox',
  props: {
    name:{
      type: String,
      required:true,
    },
    content: {
      type:[String,Number],
      required:true,
    },
    Rtype: String,
  },
  data:function(){
    return{
      checked:false,
      contentB:this.content,
    }
  },
  watch:{
    content:function(){
      this.contentB=this.content;
    }
  },
  methods:{
    change:function(){
      this.checked=1-this.checked;
    },
    submit:function(){
      if(this.contentB=="")
      {
        this.$message({
          message: '不可为空',
          type:'error',
          center:true
        });
        this.contentB=this.content;
        this.change();
      }
      else if(this.contentB==this.content)
      {
        this.change();
      }
      else
      {
        var that=this;
        if(this.Rtype=='email')
        {
          var regEmail=/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
          if(regEmail.test(this.contentB)==false)
          {
            this.$message({
              message: '邮箱格式不正确',
              type:'error',
              center:true
            });
          }
          else
          {
            var info={[this.name]:this.contentB};
            api.modify_user_info(info).then(
              function(e){
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
            this.$emit('update');
            this.change();
          }
        }
        else if(this.Rtype=='tel')
        {
          var regPhone= 11 && /^((13|14|15|17|18)[0-9]{1}\d{8})$/;
          var regTel=/^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$/;
          if((regTel.test(this.contentB)==false)&&(regPhone.test(this.contentB)==false))
          {
            this.$message({
              message: '电话格式不正确',
              type:'error',
              center:true
            });
          }
          else
          {
            var info={[this.name]:this.contentB};
            api.modify_user_info(info).then(
              function(e){
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
            this.$emit('update');
            this.change();
          }
        }
        else if(this.Rtype=='year')
        {
          if(this.contentB<=0||this.contentB>2019)
          {
            this.$message({
              message: '年份不合法',
              type:'error',
              center:true
            });
          }
          else
          {
            var info={[this.name]:this.contentB};
            api.modify_user_info(info).then(
              function(e){
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
            this.$emit('update');
            this.change();
          }
        }
        else
        {
          var info={[this.name]:this.contentB};
          api.modify_user_info(info).then(
            function(e){
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
          this.$emit('update');
          this.change();
        }
      }
    }
  }
}
</script>

<style scoped>
  .mod-col{
    height: 100%;
  }
  .mod-row{
    height: 100%;
    width: 100%;
  }
  #wenben{
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
    width: 100%;
    height: 40px;
    line-height: 40px;
  }
</style>
