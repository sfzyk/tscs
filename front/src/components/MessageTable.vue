<template>
  <div>
    <div style="margin-top:20px"></div>
    <ul class="mestable" style="width:80%;list-style-type:none;">
      <li
        v-for="item in noticelist.slice((currentpage- 1)*pagesize,currentpage*pagesize)"
        :key="item.id"
        style="margin-top:15px"
      >
        <el-row :gutter="20">
          <el-col :span="10">
            <div>{{item.time}}</div>
          </el-col>
          <el-col :span="10">
            <div>
              <router-link v-bind:to="{path:'noticeinfo',query:{id:item.id}}">{{ item.title }}</router-link>
            </div>
          </el-col>
        </el-row>
      </li>
    </ul>
    <div class="block">
      <!-- <span class="demonstration">页数较少时的效果</span> -->
      <el-pagination
        layout="prev, pager, next"
        :total="noticelist.length"
        :page-size="pagesize"
        :current-page="currentpage"
        :pager-count="5"
        @current-change="handleCurrentChange"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import api from "@/api/apis";
export default {
  data() {
    return {
      notice_id: "",
      noticelist: [],
      currentpage: 1,
      pagesize: 13
    };
  },
  created: function() {
    var that = this;
    api.get_notice_list().then(function(e) {
      var res = e["data"]["data"];
      var len = res.length;
      
      for (var i = 0; i < len; i++) {
        that.noticelist.push(res[i]);
      }
      if (len == 0) len = that.pagesize;
      if (len % that.pagesize > 0 || len == 0) {
        for (var i = 0; i < that.pagesize - (len % that.pagesize); i++) {
          that.noticelist.push({
            id:"-",
            time:"-",
            title:"",
          });
        }
      }
      console.log(that.noticelist[0]["id"]);
    });
  },
  methods: {
    handleCurrentChange(cur) {
      this.currentpage = cur;
    }
  }
};
</script>

<style scoped>
.mestable {
  margin: 15px auto 0 auto;
  height: 30%;
}
</style>