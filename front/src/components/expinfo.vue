<template>
  <div class="bodycontainer">
    <el-card>
      <div
        style="width: 95%; height: 60px;font-size: 20px; text-align: left; margin-left: 5%;margin-top: 20px;"
      >{{tab}}</div>
      <div class="rightbody">
        <el-row :gutter="20" style="margin-top: 10%;">
          <el-col :span="6">
            <div class="linehead">姓名:</div>
          </el-col>
          <el-col :span="18">
            <div class="linebody">
              <div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{name}}</div>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 5%;">
          <el-col :span="6">
            <div class="linehead">院系:</div>
          </el-col>
          <el-col :span="18">
            <div class="linebody">
              <div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{department}}</div>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 5%;">
          <el-col :span="6">
            <div class="linehead">领域:</div>
          </el-col>
          <el-col :span="18">
            <div class="linebody">
              <div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{field}}</div>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 5%;">
          <el-col :span="6">
            <div class="linehead">电话:</div>
          </el-col>
          <el-col :span="18">
            <div class="linebody">
              <div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{telephone}}</div>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 5%;">
          <el-col :span="6">
            <div class="linehead">邮箱:</div>
          </el-col>
          <el-col :span="18">
            <div class="linebody">
              <div style="height: 100%;width: 100%;line-height: 40px; text-align: left;">{{email}}</div>
            </div>
          </el-col>
        </el-row>
        <!--用相应的输入来代替原本的输入框-->
      </div>
    </el-card>
  </div>
</template>

<script>
import api from "@/api/apis";

export default {
  name: "expInfo",
  components: {
  },
  data: function() {
    return {
      tab: "个人信息",
      clear: false,
      id: 0,
      name: "",
      field: "",
      telephone: "",
      email: "",
      department: ""
    };
  },
  created: function() {
    this.initdata();
  },
  methods: {
    initdata: function() {
      var that = this;
      api.expert_info().then(function(res) {
        console.log(res);
        that.id = res["data"]["data"]["id"];
        that.name = res["data"]["data"]["name"];
        that.field = res["data"]["data"]["field"];
        that.telephone = res["data"]["data"]["telephone"];
        that.email = res["data"]["data"]["email"];
        that.department = res["data"]["data"]["college"];
      }); 
    },
  }
};
</script>

<style scoped>
.bodycontainer {
  margin: 0px 145px 20px 145px;
  height: 800px;
}
/deep/.el-tabs__header {
  width: 200px;
}
/deep/.el-tabs__nav {
  margin-top: 80px;
}
/deep/.el-tabs__item {
  height: 60px;
  font-size: 18px;
  text-align: center;
  line-height: 60px;
}
/deep/.el-tabs--left .el-tabs__item.is-left {
  text-align: center;
}
/deep/.el-tabs__content {
  text-align: center;
}
.linehead {
  height: 40px;
  width: 100%;
  text-align: center;
  line-height: 40px;
  text-align: left;
}
.linebody {
  height: 40px;
  width: 100%;
  text-align: left;
}
.rightbody {
  width: 600px;
  margin: 30px auto;
}
.rightbody2 {
  margin: 30px 0px;
}
</style>
