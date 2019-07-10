<template>
  <div class="home" align="center">
    <div class="bdy">
      <!-- type==0 All；type==1 Stu -->
      <ProjectList
        :prolist="this.prolist"
        :Spagesize="this.pagesize"
        :pagetotal="total"
        title="已提交作品"
        @pagechange="show"
        type="0"
        @search="search"
      ></ProjectList>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ProjectList from "@/components/ProjectList.vue";
import api from "@/api/apis.js";
export default {
  name: "Allproject",
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
      pagesize: 10,
      total: 0
    };
  },
  created() {
    var that = this;
    api.admin_get_projects(0, this.pagesize, this.info).then(function(result) {
      that.prolist = result["data"]["data"]["data"];
      var l = that.prolist.length;
      if (l % that.pagesize != 0) {
        for (var i = 0; i < that.pagesize - (l % that.pagesize); i++) {
          that.prolist.push({ id: 0 });
        }
      }
      that.total = result["data"]["data"]["num"];
    });
    // api.adminlogin("bbb@ccc.com", "aaa").then(function (e) {
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
      api
        .admin_get_projects(0, this.pagesize, this.info)
        .then(function(result) {
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
      console.log(val);
      api
        .admin_get_projects(val - 1, this.pagesize, this.info)
        .then(function(result) {
          console.log(result);
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
    }
  }
};
</script>
<style scoped>
.bdy {
  width: 60%;
}
</style>
