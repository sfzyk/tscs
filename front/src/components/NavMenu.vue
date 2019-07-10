<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect1"
      background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" v-if="this.$store.state.isWho === '1' ">
      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="2">参加比赛</el-menu-item>
      <!-- <el-menu-item index="3">作品管理</el-menu-item> -->
      <el-menu-item index="4">个人信息</el-menu-item>
      <el-menu-item index="5" v-show='this.$store.state.isLog' active-text-color="#fff">登出</el-menu-item>
      <el-menu-item index="6" v-show='!this.$store.state.isLog'>登录</el-menu-item>
    </el-menu>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect2"
      background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" v-if="this.$store.state.isWho=== '2' ">
      <el-menu-item index="1">首页</el-menu-item>
      <!-- <el-menu-item index="2">参加比赛</el-menu-item> -->
      <el-menu-item index="3">作品评价</el-menu-item>
      <el-menu-item index="4">个人信息</el-menu-item>
      <el-menu-item index="5" v-show='this.$store.state.isLog' active-text-color="#fff">登出</el-menu-item>
      <el-menu-item index="6" v-show='!this.$store.state.isLog'>登录</el-menu-item>
    </el-menu>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect3"
      background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" v-if="this.$store.state.isWho=== '3' ">
      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="7">查看比赛</el-menu-item>
      <el-menu-item index="2">作品审核</el-menu-item>
      <el-menu-item index="3">评委管理</el-menu-item>
      <el-menu-item index="4">发布通知</el-menu-item>
      <el-menu-item index="8">系统管理</el-menu-item>
      <el-menu-item index="5" v-show='this.$store.state.isLog' active-text-color="#fff">登出</el-menu-item>
      <el-menu-item index="6" v-show='!this.$store.state.isLog'>登录</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import api from "@/api/apis";
import store from "@/store";
export default {
  store,
  data() {
    return {
      activeIndex: "0"
    };
  },
  methods: {
    handleSelect1(key) {
      var that = this;
      if (key === "1") {
        this.$router.push("/Homepage");
      } else if (key === "2") {
        this.$router.push("/StuConList");
      }
      else if (key === "3") {
        this.$router.push("/Stuproject");
      } else if (key === "4") {
        this.$router.push("/Userinfo");
      } else if (key === "5") {
        this.activeIndex = "0";
        api.logout().then(function() {
          store.commit("setOffline");
          store.commit("isStu");
          that.$router.push("/");
        });
      } else if (key == "6") {
        this.activeIndex = "0";
        this.$router.push("/");
      }
    },
    handleSelect2(key) {
      var that = this;
      if (key === "1") {
        this.$router.push("/Homepage");
      } else if (key === "3") {
        this.$router.push({
          path:'/Expproject'
        }
          );
      } else if (key === "4") {
        this.$router.push("/ExpertInfo");
      } else if (key === "5") {
        this.activeIndex = "0";
        api.expert_logout().then(function() {
          store.commit("setOffline");
          store.commit("isStu");
          that.$router.push("/");
        });
      } else if (key == "6") {
        this.activeIndex = "0";
        this.$router.push("/");
      }
    },
    handleSelect3(key) {
      var that = this;
      if (key === "1") {
        this.$router.push("/Homepage");
      } else if (key === "2") {
        this.$router.push("/Allproject");
      } else if (key === "3") {
        this.$router.push("/ManageExp");
      }else if(key=="4"){
        this.$router.push('/notice');
      }
       else if (key === "5") {
        this.activeIndex = "0";
        api.admin_logout().then(function() {
          store.commit("setOffline");
          store.commit("isStu");
          that.$router.push("/");
        });
      } else if (key == "6") {
        this.activeIndex = "0";
        this.$router.push("/");
      }
      else if (key == "7") {
        this.activeIndex = "0";
        this.$router.push("/ContestList");
      }
      else if (key == "8") {
        this.activeIndex = "0";
        this.$router.push("/config");
      }
    }
    
  }
};
</script>
