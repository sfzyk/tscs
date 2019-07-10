<template>
  <div>

    <el-card style="opacity:0.6">
<!--      <el-row>-->
<!--        <el-col :span="1" :offset="2">-->
<!--          <div style="font-size: 20px; height:50px;background-color:#BEE"></div>-->
<!--        </el-col>-->
<!--        <el-col :span="20">-->
<!--          <div style="font-size: 20px; height:50px;background-color:#BEE" align="left">-->
<!--            <div-->
<!--              style="top: 50%;-->
<!--            transform: translateY(40%);;background-color:#BEE"-->
<!--            >{{title}}</div>-->
<!--          </div>-->
<!--        </el-col>-->
<!--      </el-row>-->
      <el-row>
        <div style="height:10px"></div>
        <el-col :span="7" :offset="14">
          <el-input placeholder="请输入内容" prefix-icon="el-icon-search" v-model="searchword"></el-input>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" icon="el-icon-search" @click="searchFunction">搜索</el-button>
        </el-col>
      </el-row>
      <div align="center">
        <el-row>
          <div style="height:10px"></div>
          <el-col :span="4" :offset="2">
            <div style="font-size: 15px;height:50px;" align="center">
              <sortButton ref="name_button" appearance="项目名称" @change-sort="sort_name"></sortButton>
            </div>
          </el-col>
          <el-col :span="4">
            <div style="font-size: 15px;" align="center">
              <sortButton ref="stu_button" appearance="申报人" @change-sort="sort_stu"></sortButton>
            </div>
          </el-col>
          <el-col :span="4">
            <div style="font-size: 15px;" align="center">
              <sortButton ref="id_button" appearance="项目编号" @change-sort="sort_id"></sortButton>
            </div>
          </el-col>
          <el-col :span="4">
            <div style="font-size: 15px;" align="center">
              <sortButton ref="cat_button" appearance="项目类别" @change-sort="sort_cat"></sortButton>
            </div>
          </el-col>
          <el-col :span="4">
            <div style="font-size: 15px;" align="center">
              <sortButton ref="sta_button" appearance="项目状态" @change-sort="sort_sta"></sortButton>
            </div>
          </el-col>
        </el-row>
      </div>
      <el-row>
        <div style="height:10px"></div>
        <el-col :span="4" :offset="2">
          <el-input placeholder prefix-icon="el-icon-search" v-model="searchname"></el-input>
        </el-col>
        <el-col :span="4" :offset="0">
          <el-input placeholder prefix-icon="el-icon-search" v-model="searchstu"></el-input>
        </el-col>
        <el-col :span="4" :offset="0">
          <el-input placeholder prefix-icon="el-icon-search" v-model="searchid"></el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchcategory" placeholder>
            <el-option
              v-for="item in opt_categories"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchstate" placeholder>
            <el-option
              v-for="item in opt_states"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <div v-for="(project) in prolist" :key="project.id" align="center">
        <div align="center">
          <el-row>
            <el-col :span="3" :offset="2">
              <div style="font-size: 15px; height:20px; " align="center">
                <router-link
                  :to="{ path:'/expertApplyInfo', query: { id: project.id }}"
                  v-if="type=='2'"
                >{{project.full_name}}</router-link>
                <router-link
                  :to="{ path:'/stuApplyInfo', query: { id: project.id }}"
                  v-if="type=='1'"
                >{{project.full_name}}</router-link>
                <router-link
                  :to="{ path:'/adminApplyInfo', query: { id: project.id }}"
                  v-else-if="type=='0'"
                >{{project.full_name}}</router-link>
              </div>
            </el-col>
            <el-col :span="4">
              <div
                style="font-size: 15px;"
                align="center"
                v-if="project.id!=0"
              >{{project.student_name}}</div>
            </el-col>
            <el-col :span="4">
              <div style="font-size: 15px;" align="center" v-if="project.id!=0">{{project.id}}</div>
            </el-col>
            <el-col :span="4">
              <div
                style="font-size: 15px;"
                align="center"
                v-if="project.id!=0"
              >{{categories[project.category]}}</div>
            </el-col>
            <el-col :span="4">
              <div
                style="font-size: 15px;"
                align="center"
                v-if="project.id!=0"
              >{{states[project.state]}}</div>
            </el-col>
            <el-col :span="3">
              <div style="height:10px" align="center" v-if="project.id!=0 && project.state===0">
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="del(project.id)"
                ></el-button>
              </div>
            </el-col>
          </el-row>
        </div>
        <el-divider></el-divider>
      </div>
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="Spagesize"
        :current-page="cur"
        :pager-count="9"
        @current-change="handleCurrentChange"
        :page-count="pagetotal"
      ></el-pagination>
      <!-- :hide-on-single-page="true" -->
    </el-card>

  </div>
</template>


<script>
  import router from "@/router";
  import api from "@/api/apis.js";
  import sortButton from "@/components/sortButton.vue";
  export default {
    name: "ConProjectList",
    props: {
      prolist: String,
      Spagesize: Number,
      title: String,
      pagetotal: Number,
      type: String
    },
    components: {
      sortButton
    },
    watch: {
      searchname: function(newval, oldval) {
        this.searchFunction();
      },
      searchstu: function(newval, oldval) {
        this.searchFunction();
      },
      searchid: function(newval, oldval) {
        this.searchFunction();
      },
      searchcategory: function(newval, oldval) {
        this.searchFunction();
      },
      searchstate: function(newval, oldval) {
        this.searchFunction();
      }
    },
    data() {
      return {
        searchname: "",
        searchstu: "",
        searchid: "",
        searchcategory: -1,
        searchstate: -1,
        sortfield: "id",
        sortorder: "0",
        searchword: "",
        jump_path: "temp",
        ScurrentPage: 1,
        cur: 1,
        states: [
          "暂存中",
          "等待初审",
          "初审通过等待专家评审",
          "专家评审通过",
          "等待答辩",
          "未晋级"
        ],
        opt_states: [
          {
            label: "--------",
            value: -1
          },
          {
            label: "暂存中",
            value: 0
          },
          {
            label: "等待初审",
            value: 1
          },
          {
            label: "初审通过等待专家评审",
            value: 2
          },
          {
            label: "专家评审通过",
            value: 3
          },
          {
            label: "等待确定答辩名单",
            value: 4
          },
          {
            label: "进入答辩名单",
            value: 5
          }
        ],
        opt_categories: [
          {
            label: "--------",
            value: -1
          },
          {
            label: "未选择",
            value: 0
          },
          {
            label: "机器与控制",
            value: 1
          },
          {
            label: "信息技术",
            value: 2
          },
          {
            label: "数理",
            value: 3
          },
           {
            label: "生命科学",
            value: 4
          },
          {
            label: "能源化工",
            value: 5
          },
          {
            label: "哲学社会科学",
            value: 6
          }
        ],
        categories: [
          "未选择",
          "机器与控制",
          "信息技术",
          "数理",
          "生命科学",
          "能源化工",
          "哲学社会科学"
        ]
      };
    },
    methods: {
      sort_name(sort_type) {
        console.log(sort_type);
        this.sortfield = "full_name";
        this.sortorder = sort_type;
        this.searchFunction();
        this.$refs.contest_button.clear();
        this.$refs.stu_button.clear();
        this.$refs.id_button.clear();
        this.$refs.cat_button.clear();
        this.$refs.sta_button.clear();
      },
      sort_stu(sort_type) {
        console.log(sort_type);
        this.sortfield = "name";
        this.sortorder = sort_type;
        this.searchFunction();
        this.$refs.contest_button.clear();
        this.$refs.name_button.clear();
        this.$refs.id_button.clear();
        this.$refs.cat_button.clear();
        this.$refs.sta_button.clear();
      },
      sort_id(sort_type) {
        console.log(sort_type);
        this.sortfield = "id";
        this.sortorder = sort_type;
        this.searchFunction();
        this.$refs.contest_button.clear();
        this.$refs.stu_button.clear();
        this.$refs.name_button.clear();
        this.$refs.cat_button.clear();
        this.$refs.sta_button.clear();
      },
      sort_sta(sort_type) {
        console.log(sort_type);
        this.sortfield = "state";
        this.sortorder = sort_type;
        this.searchFunction();
        this.$refs.contest_button.clear();
        this.$refs.stu_button.clear();
        this.$refs.id_button.clear();
        this.$refs.cat_button.clear();
        this.$refs.name_button.clear();
      },
      sort_cat(sort_type) {
        console.log(sort_type);
        this.sortfield = "category";
        this.sortorder = sort_type;
        this.searchFunction();
        this.$refs.contest_button.clear();
        this.$refs.stu_button.clear();
        this.$refs.id_button.clear();
        this.$refs.name_button.clear();
        this.$refs.sta_button.clear();
      },
      searchFunction() {
        this.$emit(
          "search",
          this.searchword,
          this.searchname,
          this.searchstu,
          this.searchid,
          this.searchcategory,
          this.searchstate,
          this.sortfield,
          this.sortorder
        );
      },
      handleCurrentChange(currentPage) {
        this.cur = currentPage;
        this.$emit("pagechange", currentPage);
      },
      del(id) {
        var that = this;
        this.$confirm("此操作将永久删除该文件, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            this.$message({
              type: "success",
              message: "删除成功!"
            });
            api.delete_application(id).then(function(result) {
              that.$emit("pagechange", that.cur);
            });
          })
          .catch(() => {});
      }
    },
    created() {
      console.log(this.prolist);
      console.log(this.type);
      this.prolist = JSON.parse(this.prolist);
    }
  };
</script>
