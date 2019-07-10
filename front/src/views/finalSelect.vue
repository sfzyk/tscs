<template>
  <el-card class="spspcard">

    <el-table :data="tableData" style="margin:0 auto" ref="finallist" @selection-change="handleSelectionChange"
      height="500" @row-click="clickRow">
      <el-table-column type="selection" width="100">
      </el-table-column>
      <el-table-column type="index" width="150" :index="indexMethod">
      </el-table-column>
      <el-table-column prop="name" label="项目名称" width="500">
      </el-table-column>
      <el-table-column prop="score" label="分数">
      </el-table-column>
    </el-table>

    <el-row>
      <el-col :span="3">
        <el-button @click="enter">提交</el-button>
      </el-col>
      <el-col :span="3">
        <el-button @click="stage">保存</el-button>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import api from "@/api/apis.js";
export default {
  name: "FinalSelect",
  data() {
    return {
      tableData: [{ id: "", score: "", isSel: "", name: "" }],
      contest_id: "",
      multipleSelection: []
    };
  },
  created() {
    this.contest_id = this.$route.query.contest_id;
    this.getList();
  },
  methods: {
    clickRow(val) {
      this.currentRow = val
      this.$router.push({path:"/adminApplyInfo",query:{id:val.id}});
    },
    getList() {
      var that = this;
      api.get_final(this.contest_id).then(function(e) {
        var d = eval(e["data"]["data"]);
        that.tableData = [];
        for (var j = 0; j < d.length; j++) {
          that.tableData.push({
            id: d[j][0],
            score: d[j][1],
            isSel: d[j][2],
            name: d[j][3]
          });
        }
        that.$nextTick(function() {
          that.checked(); //每次更新了数据，触发这个函数即可。
        });
      });
    },
    checked() {
      for (var i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].isSel === 1) {
          this.$refs.finallist.toggleRowSelection(this.tableData[i], true);
        }
      }
    },
    indexMethod(index) {
      return index + 1;
    },
    reflshTable() {
      this.getList();
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    stage(){
      console.log(this.multipleSelection)
      var ids=[]
      for (var i = 0; i < this.multipleSelection.length; i++) {
        ids.push(this.multipleSelection[i].id)
      }
      api.stage_final(this.contest_id,JSON.stringify(ids)).then(function(){
      })
    },
    enter(){
      var ids=[]
      var that=this
      for (var i = 0; i < this.multipleSelection.length; i++) {
        ids.push(this.multipleSelection[i].id)
      }
      api.enter_final(this.contest_id,JSON.stringify(ids)).then(function(e){
        if(e["data"]["code"]==200)
        {
          that.$message("提交成功")
        }
        else if(e["data"]["code"]==210){
          that.$message("不可重复提交")
        }
        
      })
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
.spspcard {
  width: 70%;
  margin: 0 auto;
}
</style>
