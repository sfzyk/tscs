<template>
  <div class="body">
    <el-card class="box-card-login" :style="note" v-show="!isReg">
      <div class="login-inner">
        <el-avatar :size="60" :src="circleUrl"></el-avatar>
        <el-row style="margin-top: 2%">
          <el-col :span="6">
            <div class="tips">邮箱：</div>
          </el-col>
          <el-col :span="18">
            <el-input v-model="email" placeholder="请输入邮箱" :disabled="true"></el-input>
          </el-col>
        </el-row>
        <el-row style="margin-top: 12%">
          <el-col :span="6">
            <div class="tips">领域：</div>
          </el-col>
          <el-col :span="18">
            <el-select
              v-model="value"
              size="medium"
              empty="数理"
              filterable
              class="field"
              allow-create
              default-first-option
              placeholder="请选择研究领域"
            >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-col>
        </el-row>
        <el-row style="margin-top: 12%">
          <el-col :span="6">
            <div class="tips">姓名：</div>
          </el-col>
          <el-col :span="18">
            <el-input v-model="name" placeholder="请输入姓名" :disabled="false"></el-input>
          </el-col>
        </el-row>
        <el-row style="margin-top: 12%">
          <el-col :span="6">
            <div class="tips">密码：</div>
          </el-col>
          <el-col :span="18">
            <el-input v-model="password" placeholder="请输入密码" show-password></el-input>
          </el-col>
        </el-row>
        <el-row style="margin-top: 12%">
          <el-col :span="6" :offset="10">
            <el-button type="primary"  @click="reset">重置密码</el-button>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>
<script>
import api from "@/api/apis.js";
export default {
  data() {
    return {
      id: "",
      email: "realvicco@outlook.com",
      field: "",
      name: "王二小",
      password: "",
      circleUrl:
        "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
      note: {
        backgroundImage: "url(" + require("@/assets/p6.jpg") + ")",
        backgroundRepeat: "no-repeat"
      },
      options: [
        {
          value: "1",
          label: "机械与控制"
        },
        {
          value: "2",
          label: "信息技术"
        },
        {
          value: "3",
          label: "数理"
        },
        {
          value: "4",
          label: "能源化工"
        },
        {
          value: "5",
          label: "哲学社会科学"
        }
      ],
      value: "信息技术"
    };
  },
  created: function() {
    var that = this;
    this.id = this.$route.query.id;
    api.invitation_info(this.id).then(function(e) {
      var res = e["data"]["data"];
      if (res["state"] == 1) that.$router.push("/Homepage");
      else {
        that.name = res["name"];
        that.email = res["email"];
        that.field = res["field"];
      }
    });
  },
  methods: {
    reset() {
      console.log("2222222222222222222222222");
      if (this.password == "") {
        this.$message("请输入密码");
      } else {
        var that = this;
        console.log("reset");
        api
          .invitation_reset({
            uni_link: that.id,
            join: 0,
            password: that.password
          })
          that.$router.push("/");
      }
    }
  }
};
</script>

<style scoped>
.body {
  margin: 70px auto 150px auto;
}
.field {
  width: 266px;
}
.el-main {
  /* background-color: #e9eef3; */
  color: #333;
  width: 60%;
  /* text-align: center; */
  /* line-height: 160px; */
}
.login-outer {
  height: 50%;
  width: 60%;
  margin: 5px auto 150px auto;
}
.tips {
  margin-top: 15%;
  font-size: 16px;
}
.login-inner {
  height: 100%;
  width: 100%;
}
.box-card-login {
  width: 400px;
  height: 480px;
  margin: 5px auto 150px auto;
}
</style>
