<template>
  <el-card class="spcard">
    <div class="spsearchbar">
      <el-row type="flex" justify="end">
        <el-col :span="12">
          <el-input placeholder="请输入内容" v-model="input">
            <el-select v-model="select" slot="prepend" placeholder="请选择" style="width:12vh">
              <el-option label="姓名" value="name"></el-option>
              <el-option label="专业" value="field"></el-option>
              <el-option label="院系" value="college"></el-option>
              <el-option label="邮箱" value="email"></el-option>
              <el-option label="联系电话" value="telephone"></el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" @click="search" class="searchbutton"></el-button>
          </el-input>
        </el-col>
        <el-col :span="3">
          <el-button @click="cancelSS">取消</el-button>
        </el-col>
      </el-row>

    </div>

    <el-table :data="tableData" style="margin:0 auto" ref="explist" highlight-current-row @row-click="clickRow"
      @sort-change='sort'>
      <el-table-column type="index" width="80" :index="indexMethod">
      </el-table-column>
      <el-table-column prop="name" label="姓名" width="200" :sortable='sortType'>
      </el-table-column>
      <el-table-column prop="field" label="专业" width="200" :sortable='sortType'>
      </el-table-column>
      <el-table-column prop="college" label="院系" width="200" :sortable='sortType'>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" width="200" :sortable='sortType'>
      </el-table-column>
      <el-table-column prop="telephone" label="联系电话" :sortable='sortType'>
      </el-table-column>
    </el-table>
    <el-pagination @current-change="handleCurrentPageChange" :current-page.sync="currentPage" :page-size='pageSize'
      layout="prev, pager, next, jumper" :total='totalItem'>
    </el-pagination>
  </el-card>
</template>

<script>
import api from "@/api/apis.js";
export default {
  data() {
    return {
      select: "",
      input: "",
      sortType: "custom",
      currentRow: null,
      pageSize: 5,
      totalItem: null,
      currentPage: 1,
      tableData: [],
      fieldSiwch: [
        "A.机械控制",
        "B.信息技术",
        "C.数理",
        "D.生命科学",
        "E.能源化工",
        "F.哲学社会科学"
      ],
      info: {
        field: "",
        order: "",
        search: "{}"
      }
    };
  },
  created() {
    this.info.field = "";
    this.info.order = "";
    this.info.search = "{}";
    this.getExp(0);
  },
  methods: {
    getExp(pageNum) {
      var that = this;
      api.get_experts(pageNum, this.pageSize, this.info).then(function(result) {
        var d = eval(result["data"]["data"]["data"]);
        that.tableData = [];
        for (var j = 0; j < d.length; j++) {
          that.tableData.push(JSON.parse(d[j]));
          that.tableData[j].field =
            that.fieldSiwch[parseInt(that.tableData[j].field)];
        }
        that.totalItem = result["data"]["data"]["num"] * that.pageSize;
        if(that.currentPage>result["data"]["data"]["num"]){
          that.currentPage=that.currentPage-1
          that.getExp(that.currentPage-1)
        }
      });
    },
    indexMethod(index) {
      return index + 1 + (this.currentPage - 1) * this.pageSize;
    },
    clickRow(val) {
      this.currentRow = val;
      this.$emit("clickRow", val);
    },
    reflshTable() {
      this.getExp(this.currentPage - 1);
    },
    cancel(row) {
      this.$refs.explist.setCurrentRow(row);
    },
    handleCurrentPageChange(val) {
      this.$emit("pageChange");
      this.getExp(val - 1);
    },
    sort(column) {
      this.info.field = column["prop"];
      if (column["order"] == "ascending") {
        this.info.order = 1;
      } else if (column["order"] == "descending") {
        this.info.order = 2;
      } else {
        this.info.order = 0;
      }

      this.getExp(0);
      this.currentPage = 1;
    },
    search() {
      var search = {};
      search[this.select] = this.input;
      this.info.search = JSON.stringify(search);
      this.getExp(0);
      this.currentPage = 1;
    },
    cancelSS() {
      this.info.field = "";
      this.info.order = "";
      this.info.search = "{}";
      this.select = "";
      this.input = "";
      this.getExp(0);
      this.currentPage = 1;
    }
  }
};
</script>

<style>
.spsearchbar {
  width: 100vh;
  margin: 0 0 0 auto;
}
.searchbutton {
  margin: 10px;
}
</style>
