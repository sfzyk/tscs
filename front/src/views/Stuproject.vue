<template>
  <div class="home" align="center">
    <div class="bdy">
      <!-- type==0 All；type==1 Stu -->
      <ProjectList
        :prolist="prolist"
        :Spagesize="pagesize"
        :pagetotal="total"
        title="我的作品"
        @pagechange="show"
        type="1"
        @search="search"
        ref="projects"
      ></ProjectList>
    </div>
    <div style="height:100px; width:80%; background-color:white; opacity:0.6">
      <el-button type="primary" round icon="el-icon-circle-plus-outline" @click="addproject">添加项目</el-button>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ProjectList from "@/components/ProjectList.vue";
import api from "@/api/apis.js";
export default {
  name: "Stuproject",
  components: {
    ProjectList
  },
  data() {
    return {
      info: {
        field: "id",
        order: "0",
        search: JSON.stringify("{}")
      },
      prolist: [],
      pagesize: 8,
      total: 0
    };
  },
  created() {
    var that = this;
    api
      .student_get_projects(0, this.pagesize, this.info)
      .then(function(result) {
        console.log(result);
        console.log(result["data"]["data"]["data"]);
        that.prolist = result["data"]["data"]["data"];
        var l = that.prolist.length;
        if (l % that.pagesize != 0) {
          for (var i = 0; i < that.pagesize - (l % that.pagesize); i++) {
            that.prolist.push({ id: 0 });
          }
        }
        that.total = result["data"]["data"]["num"];
      });
    // api.login("123@123.com", "123").then(function (e) {
    //       console.log(e)
    //       if (e['data']['code'] === 200) {
    //         alert('登陆成功！')
    //         that.$router.push('/Homepage_adm')
    //       } else if (e['data']['code'] === 202) {
    //         alert('请将信息填写完整！')
    //       } else if (e['data']['code'] === 201) {
    //         alert('邮箱密码错误！')
    //       }
    //     })
  },
  methods: {
    search(
      searchword,
      searchname,
      searchcontest,
      searchstu,
      searchid,
      searchcategory,
      searchstate,
      sortfield,
      sortorder
    ) {
      console.log(
        searchword +
          " " +
          searchname +
          " " +
          searchcontest +
          " " +
          searchstu +
          " " +
          searchid +
          " " +
          searchcategory +
          " " +
          searchstate +
          " " +
          sortfield +
          " " +
          sortorder
      );
      this.info = {};
      var search = {};
      var that = this;
      if (searchword != "") {
        search["common_search"] = searchword;
      }
      if (searchname != "") {
        search["full_name"] = searchname;
      }
      if (searchcontest != "") {
        search["contest__name"] = searchcontest;
      }
      if (searchstu != "") {
        search["name"] = searchstu;
      }
      if (searchid != "") {
        search["id"] = searchid;
      }
      if (searchcategory != -1) {
        search["category"] = searchcategory;
      }
      if (searchstate != -1) {
        search["state"] = searchstate;
      }
      this.info["field"] = sortfield;
      this.info["order"] = sortorder;
      this.info["search"] = JSON.stringify(search);
      console.log(this.info);
      api.student_get_projects(0, this.pagesize, this.info).then(function(result) {
          console.log("王佳奇");
          console.log(result);
          console.log(result["data"]["data"]["data"]);
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
    show(val) {
      var that = this;
      api
        .student_get_projects(val - 1, this.pagesize, this.info)
        .then(function(result) {
          if (result["data"]["data"]["data"].length == 0 && val > 1) {
            that.show(val - 1);
            return;
          }
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
    addproject() {
      var that = this;
      api
        .stage_application(
          "{}", // cooperatorinfo,
          "", //email,
          "未命名项目", //fullname,
          "", //telephone,
          "", //address,
          "", //innovation
          "", //keywords,
          "0", //category,
          "", //descriptions
          "0", // education_background,
          "0", //,type,
          "['0']", //type_info
          "2"
        )
        .then(function(result) {
          var pid = result["data"]["data"];
          console.log(result);
          that.$router.push({
            path: "/stuApplyInfo",
            query: {
              id: pid
            }
          });
        });
      //this.$router.push('/applyInfo')
    }
  }
};
</script>
<style scoped>
.bdy {
  width: 80%;
}
</style>
