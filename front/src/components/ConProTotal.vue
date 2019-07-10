<template>
  <div>
    <ConProjectList v-if="priority==0" :prolist="prolist" :Spagesize="pagesize" :pagetotal="total" @pagechange="show"
      type=1 @search="search0" ref="projects"></ConProjectList>
    <ConProjectList v-if="priority==2" :prolist="prolist" :Spagesize="pagesize" :pagetotal="total" @pagechange="show"
      type=0 @search="search2" ref="projects"></ConProjectList>
  </div>
</template>

<script>
import ConProjectList from "@/components/ConProjectList.vue";
import api from "@/api/apis";
export default {
  name: "ConProTotal",
  components: {
    ConProjectList
  },
  props: {
    contest_id: {
      type: Number,
      required: true
    },
    priority: {
      type: Number,
      required: true
    }
  },
  data: function() {
    return {
      contest_info: {},
      prolist: "",
      pagesize: 8,
      total: 0,
      info: {
        field: "id",
        order: "0",
        search: JSON.stringify("{}")
      },
    };
  },
  created: function() {
    this.contest_info = this.GetInfo(this.contest_id);
    var that = this;
    if (this.priority == 2) {
      api
        .admin_get_projects(0, this.pagesize, this.contest_info)
        .then(function(result) {
          // console.log(result);
          // console.log(result["data"]["data"]["data"]);
          that.prolist = result["data"]["data"]["data"];
          var l = that.prolist.length;
          if (l % that.pagesize != 0) {
            for (var i = 0; i < that.pagesize - (l % that.pagesize); i++) {
              that.prolist.push({ id: 0 });
            }
          }
          that.total = result["data"]["data"]["num"];
        });
    } else if (this.priority == 0) {
      api
        .student_get_projects(0, this.pagesize, this.contest_info)
        .then(function(result) {
          // console.log(result);
          // console.log(result["data"]["data"]["data"]);
          that.prolist = result["data"]["data"]["data"];
          var l = that.prolist.length;
          if (l % that.pagesize != 0) {
            for (var i = 0; i < that.pagesize - (l % that.pagesize); i++) {
              that.prolist.push({ id: 0 });
            }
          }
          that.total = result["data"]["data"]["num"];
        });
    } else {
      alert("priority wrong");
    }
  },
  methods: {
    GetInfo(Cid) {
      var sea = { contest_id: Cid };
      var info = { field: "id", order: "1", search: JSON.stringify(sea) };
      return info;
    },
    search0(
      searchword,
      searchname,
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
      search['contest_id']=this.contest_id;
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
    search2(
      searchword,
      searchname,
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
      search['contest_id']=this.contest_id;
      this.info["field"] = sortfield;
      this.info["order"] = sortorder;
      this.info["search"] = JSON.stringify(search);
      console.log(this.info);
      api.admin_get_projects(0, this.pagesize, this.info).then(function(result) {
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
      //console.log(val);
      if (this.priority == 2) {
        api
          .admin_get_projects(val - 1, this.pagesize, this.contest_info)
          .then(function(result) {
            //console.log(result);
            //console.log(result["data"]["data"]["data"]);
            console.log("lenlen",result["data"]["data"]["data"].length)
            if (JSON.parse(result["data"]["data"]["data"]).length == 0 && val > 1) {
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
      } else if (this.priority == 0) {
        api
          .student_get_projects(val - 1, this.pagesize, this.contest_info)
          .then(function(result) {
            console.log("len",result["data"]["data"]["data"].length)
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
      } else {
        alert("应该是专家");
      }
    },
    dateFormat: function(time) {
      var date = new Date(time);
      var year = date.getFullYear();
      var month =
        date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1;
      var day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
      var hours =
        date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
      var minutes =
        date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
      var seconds =
        date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
      // 拼接
      return year + "年 " + month + "月 " + day + "日";
    }
  }
};
</script>

<style scoped>
</style>
