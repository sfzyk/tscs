<template>
  <el-container>
    <el-header></el-header>
    <el-container>
      <el-main>
        <transition name="el-fade-in-linear">
          <el-card class="box-card-login" :style="note" v-show="!isReg">
            <div class="login-inner">
              <el-row style="margin-top: 12%">
                <el-col :span="6">
                  <div class="tips">邮箱：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="loginEmail" placeholder="请输入邮箱"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 12%">
                <el-col :span="6">
                  <div class="tips">密码：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="loginPassword" placeholder="请输入密码" show-password></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 12%">
                <el-radio v-model="radio" label="1">学生</el-radio>
                <el-radio v-model="radio" label="2">评委</el-radio>
                <el-radio v-model="radio" label="3">校团委</el-radio>
              </el-row>
              <el-row style="margin-top: 12%">
                <el-col :span="6" :offset="4">
                  <el-button type="primary" plain @click="login()">登录</el-button>
                </el-col>
                <el-col :span="14">
                  <el-button plain @click="reg()">学生注册</el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </transition>
        <transition name="el-fade-in-linear">
          <el-card class="box-card-register" :style="note" v-show="isReg">
            <div class="login-inner">
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">姓名：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerName" placeholder="请输入姓名"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">学号：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerId" placeholder="请输入学号"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">入学年份：</div>
                </el-col>
                <el-col :span="15">
                  <el-input v-model="registerYear" placeholder="请输入入学年份"></el-input>
                </el-col>
                <el-col :span="3">
                  <div class="tips">年</div>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">专业：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerMajor" placeholder="请输入专业"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">学院：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerDepartment" placeholder="请输入学院"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">出生日期：</div>
                </el-col>
                <el-col :span="18">
                  <el-date-picker
                    v-model="registerBirth"
                    type="date"
                    placeholder="选择日期"
                    format="yyyy 年 MM 月 dd 日"
                    value-format="yyyy-MM-dd"
                    :editable="ediTable"
                    style="width:100%"
                  ></el-date-picker>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">电子邮箱：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerEmail" placeholder="请输入电子邮箱地址"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">电话号码：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerTelephone" placeholder="请输入电话号码"></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">密码：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerPassword" placeholder="请输入密码" show-password></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6">
                  <div class="tips">确认密码：</div>
                </el-col>
                <el-col :span="18">
                  <el-input v-model="registerRepassword" placeholder="请再次输入密码" show-password></el-input>
                </el-col>
              </el-row>
              <el-row style="margin-top: 5%">
                <el-col :span="6" :offset="4">
                  <el-button type="primary" plain @click="register()">确定</el-button>
                </el-col>
                <el-col :span="14">
                  <el-button plain @click="cancel()">取消</el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import api from "@/api/apis";
import store from '@/store'

export default {
  name: "Login",
  store,
  data() {
    return {
      note: {
        backgroundImage: "url(" + require("@/assets/p6.jpg") + ")",
        backgroundRepeat: "no-repeat"
      },
      isReg: false,
      ediTable: false,
      radio: "1",
      loginEmail: "",
      loginPassword: "",
      registerName: "",
      registerId: "",
      registerYear: "",
      registerMajor: "",
      registerDepartment: "",
      registerEmail: "",
      registerTelephone: "",
      registerPassword: "",
      registerRepassword: "",
      registerBirth: ""
    };
  },
  methods: {
    login() {
      var that = this;
      if (this.loginEmail === "" || this.loginPassword === "") {
        that.$message("请将信息填写完整");
      } else if (this.radio === "1") {
        api.login(this.loginEmail, this.loginPassword).then(function(e) {
          if (e["data"]["code"] === 200) {
            store.commit('setOnline')
            store.commit("isStu");
            that.$message("登陆成功！");
            that.$router.push("/Homepage");
          } else if (e["data"]["code"] === 202) {
            that.$message("请将信息填写完整！");
          } else if (e["data"]["code"] === 201) {
            that.$message("邮箱密码错误！");
          }
        });
      } else if (this.radio === "2") {
        api.expertlogin(this.loginEmail, this.loginPassword).then(function(e) {
          if (e["data"]["code"] === 200) {
            store.commit('setOnline')
            that.$message("登陆成功！");
            store.commit("isExp");
            that.$router.push("/Homepage");
          } else if (e["data"]["code"] === 202) {
            that.$message("请将信息填写完整！");
          } else if (e["data"]["code"] === 201) {
            that.$message("邮箱密码错误！");
          }
        });
      } else if (this.radio === "3") {
        api.adminlogin(this.loginEmail, this.loginPassword).then(function(e) {
          if (e["data"]["code"] === 200) {
            store.commit('setOnline')
            that.$message("登陆成功！");
            store.commit("isAdm");
            that.$router.push("/Homepage");
          } else if (e["data"]["code"] === 202) {
            that.$message("请将信息填写完整！");
          } else if (e["data"]["code"] === 201) {
            that.$message("邮箱密码错误！");
          }
        });
      }
    },
    reg() {
      this.isReg = true;
    },
    cancel() {
      this.isReg = false;
    },
    register() {
      var that = this;
      if (this.registerPassword !== this.registerRepassword) {
        that.$message("两次输入的密码不一致！");
      } else {
        if (this.registerPassword === this.registerRepassword) {
          api
            .register(
              this.registerYear,
              this.registerEmail,
              this.registerPassword,
              this.registerName,
              this.registerTelephone,
              this.registerId,
              this.registerMajor,
              this.registerDepartment,
              this.registerBirth
            )
            .then(function(e) {
              if (e["data"]["code"] === 200) {
                that.$message("注册成功！");
                that.registerYear = "";
                that.registerEmail = "";
                that.registerPassword = "";
                that.registerRepassword = "";
                that.registerName = "";
                that.registerTelephone = "";
                that.registerId = "";
                that.registerMajor = "";
                that.registerDepartment = "";
                that.registerBirth = "";
                that.isReg = false;
              } else if (e["data"]["code"] === 202) {
                that.$message("请将信息填写完整！");
              } else if (e["data"]["code"] === 204) {
                that.$message("请正确输入邮箱！");
              } else if (e["data"]["code"] === 205) {
                that.$message("请正确输入电话号码！");
              } else if (e["data"]["code"] === 207) {
                that.$message("该邮箱已注册！");
              } else if (e["data"]["code"] === 209) {
                that.$message("请正确输入出生日期！");
              }
            });
        }
      }
    }
  }
};
</script>

<style scoped>
.login-outer {
  height: 400px;
  width: 80%;
  margin-left: 5%;
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
  height: 400px;
  margin: 5px auto 150px auto;
}
.box-card-register {
  width: 400px;
  height: 700px;
  margin: 5px auto;
}
</style>
