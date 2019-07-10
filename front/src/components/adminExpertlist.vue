<template>
  <el-card class="applyInfoForm" shadow="always" style="margin: 0 auto;">
    <el-transfer v-model="value4" :props="{
      key: 'value',
      label: 'desc',
    }" :data="data3" :titles="['未选专家', '已选专家']" style="text-align:left" filterable
      filter-placeholder="请输入搜索内容">
      <div class="transfer-footer" slot="left-footer" size="small" disabled>{{icon[0]}} 未选择 {{icon[2]}} 接受 {{icon[3]}} 拒绝 {{icon[1]}} 未回复</div>
      <el-button class="transfer-footer" slot="right-footer" size="small" @click="addauto">分配专家</el-button>
    </el-transfer>
  </el-card>

</template>

<script>
import api from "@/api/apis.js";
export default {
  props :{contestid : String},
  data() {
    return {
      data3: [],
      value4: [],
      info: {
        field: "",
        order: "",
        search: "{}"
      },
      icon : ["⭐","🤔","👌","❌"],
      expertlist: [],
      totalItem: 0,
      fieldSiwch: [
        "机械控制",
        "信息技术",
        "数理",
        "生命科学",
        "能源化工",
        "哲学社会科学"
      ]
    };
  },
  methods: {
    getExpert(pageNum, pageSize, info) {
      var that = this;
      api.experts_contests(pageNum, pageSize, info ,that.contestid).then(function(result) {
        var d = eval(result["data"]["data"]["data"]);
        that.expertlist = [];
        for (var j = 0; j < d.length; j++) {
          that.expertlist.push(JSON.parse(d[j]));
          //that.expertlist[j].field = that.fieldSiwch[(that.expertlist[j].field)];
        }
        that.totalItem = result["data"]["data"]["data"].length;
        const data = [];
        for (let i = 0; i < that.totalItem; i++) {
          var inviteState=that.expertlist[i]["contest_state"]
          data.push({
            value: i,
            desc:
              that.icon[inviteState]
              +
              i +
              "-" +
              "姓名:" +
              that.expertlist[i]["name"] +
              "-邮箱:" +
              that.expertlist[i]["email"] +
              "-领域:" +
              that.fieldSiwch[that.expertlist[i]["field"]]
          });
        }
        console.log(data);
        that.data3 = data;
      });
    },
    addauto() {
      var that = this;
      var autoRes = [];
      for (var i = 0; i < this.value4.length; i++) {
        autoRes.push(that.expertlist[this.value4[i]]["id"]);
      }
      api
        .manual_dispatch(that.contestid, JSON.stringify(autoRes))
        .then(function(result) {
          console.log(result);
          if (result["data"]["code"] == "200") {
            that.$message("分配成功");
          } else if (result["data"]["code"] == "278") {
            that.$message("每个领域的人数未达到标准");
          } else {
            that.$message("分配失败");
          }
        });
      this.$emit('dispatch_change');
    }
  },
  created() {
    var that = this;
    console.log(that.contestid)
    that.getExpert(0, 500, this.info);
  }
};
</script>
<style>
.applyInfoForm {
  width: 93%;
}
.el-transfer-panel {
  width: 25% !important;
  margin: 100px
}
.transfer-footer {
  margin-left: 20px;
  padding: 6px 5px;
}
</style>
