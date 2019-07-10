<template>
  <div style="width:100%; margin: 40px auto;" v-show="isChecked[state]">
    <el-row style="margin:10px auto">
      评审专家
    </el-row>
    <el-row>
      <el-tag :key="tag.id" v-for="tag in expTags" closable :disable-transitions="false" @close="handleClose(tag)"
        style=" margin: auto 2px;">
        {{tag.name}}</el-tag>
    </el-row>
    <el-row style=" margin: 10px auto;">
      <el-button @click="showList" v-show="!isAdd">添加专家</el-button>
      <el-button @click="hideList" v-show="isAdd">取消</el-button>
    </el-row>
    <ExpList @clickRow="clickRow" v-show="isAdd"></ExpList>
  </div>
</template>
<script>
import ExpList from "@/components/ExpList.vue";
import api from "@/api/apis.js";
export default {
  name: "ProjectExpert",
  components: {
    ExpList
  },
  props: {
    state: Number,
    proId: String,
    expTags: {}
  },
  data() {
    return {
      isAdd: false,
      isChecked: [false,false,true]
    };
  },
  created() {
    
  },
  methods: {
    clickRow(val) {
      var that = this;
      api.add_to_project(val.id, this.proId).then(function(e) {
        if(e['data']['code']===200){
          that.expTags.push({relation_id:e['data']['data'],name: val.name, id: val.id });
        }
      });
    },
    handleClose(tag) {
      var that = this;
      api.delete_from_project(tag.relation_id).then(function(e) {
        if(e['data']['code']===200){
          that.expTags.splice(that.expTags.indexOf(tag), 1);
        }
      });
    },
    showList() {
      this.isAdd = true;
    },
    hideList() {
      this.isAdd = false;
    }
  }
};
</script>
