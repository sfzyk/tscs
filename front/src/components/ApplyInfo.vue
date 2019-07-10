<template>
  <div>
    <div slot="header">
      <span>申请表信息</span>
    </div>
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="80px"
      :inline="true"
      style="width:100%"
      label-position="right"
    >
      <br />
      <el-form-item label="姓名" prop="name">
        <el-input v-model="ruleForm.name" class="Input" :disabled="true"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="学号" prop="stuid">
        <el-input v-model="ruleForm.stuid" class="Input" :disabled="true"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="出生日期">
        <el-form-item prop="date1">
          <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date1" :disabled="true"></el-date-picker>
        </el-form-item>
      </el-form-item>
      <el-form-item label="入学年份">
        <el-form-item prop="year">
          <el-input v-model="ruleForm.year" :disabled="true"></el-input>
        </el-form-item>
      </el-form-item>
      <br />
      <el-form-item label="专业" prop="major">
        <el-input v-model="ruleForm.major" class="Input" :disabled="true"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="联系电话" prop="phone">
        <el-input v-model="ruleForm.phone" class="Input" :disabled="limit"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="ruleForm.email" class="Input" :disabled="limit"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="现学历" prop="eduBackground">
        <el-select
          v-model="ruleForm.eduBackground"
          placeholder="请选择学历"
          class="Input"
          :disabled="limit"
        >
          <el-option label="未选择" value="0"></el-option>
          <el-option label="A 大专" value="1"></el-option>
          <el-option label="B 大学本科" value="2"></el-option>
          <el-option label="C 硕士研究生" value="3"></el-option>
          <el-option label="D 博士研究生" value="4"></el-option>
        </el-select>
      </el-form-item>
      <br />
      <el-form-item label="作品全称" prop="projectName">
        <el-input v-model="ruleForm.projectName" class="Input" :disabled="limit"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="通讯地址" prop="address">
        <el-input v-model="ruleForm.address" class="Input" :disabled="limit"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="作品分类" prop="projectClass">
        <el-select
          v-model="ruleForm.projectClass"
          placeholder="请选择分类"
          class="Input"
          :disabled="limit"
        >
          <el-option label="未选择" value="0"></el-option>
          <el-option label="A 机器与控制" value="1"></el-option>
          <el-option label="B 信息技术" value="2"></el-option>
          <el-option label="C 数理" value="3"></el-option>
          <el-option label="D 生命科学" value="4"></el-option>
          <el-option label="E 能源化工" value="5"></el-option>
          <el-option label="F 哲学社会科学" value="6"></el-option>
        </el-select>
      </el-form-item>
      <br />
      <el-form-item label="作品说明" prop="descriptions">
        <el-input
          v-model="ruleForm.descriptions"
          class="Input"
          type="textarea"
          :autosize="{minRows:3,maxRows:10}"
          :disabled="limit"
          maxlength="800"
          show-word-limit
        ></el-input>
      </el-form-item>
      <br />
      <el-form-item label="创新说明" prop="innovation">
        <el-input
          v-model="ruleForm.innovation"
          class="Input"
          type="textarea"
          :autosize="{minRows:3,maxRows:10}"
          :disabled="limit"
        ></el-input>
      </el-form-item>
      <br />
      <el-form-item label="关键字" prop="keywords">
        <el-input v-model="ruleForm.keywords" placeholder="关键字按、隔开" class="Input" :disabled="limit"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="作品类别" prop="type">
        <el-select v-model="ruleForm.type" placeholder="请选择类别" class="Input" :disabled="limit">
          <el-option label="未选择" value="0"></el-option>
          <el-option label="A 科技发明制作" value="1"></el-option>
          <el-option label="B 调查报告和学术论文" value="2"></el-option>
        </el-select>
      </el-form-item>
      <br />
      <el-form-item label="展示形式" prop="display" v-show="ruleForm.type == '1' ">
        <el-checkbox-group v-model="ruleForm.display" :disabled="limit">
          <el-checkbox label="0" v-show="false">默认</el-checkbox>
          <el-checkbox label="1">实物、产品</el-checkbox>
          <el-checkbox label="2">模型</el-checkbox>
          <el-checkbox label="3">图纸</el-checkbox>
          <el-checkbox label="4">磁盘</el-checkbox>
          <el-checkbox label="5">现场演示</el-checkbox>
          <el-checkbox label="6">图片</el-checkbox>
          <el-checkbox label="7">录像</el-checkbox>
          <el-checkbox label="8">样品</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <br />
      <el-form-item label="调查方式" prop="investigate" v-show="ruleForm.type == '2' ">
        <el-checkbox-group v-model="ruleForm.investigate" :disabled="limit">
          <el-checkbox label="0" v-show="false">默认</el-checkbox>
          <el-checkbox label="1">走访</el-checkbox>
          <el-checkbox label="2">问卷</el-checkbox>
          <el-checkbox label="3">现场采访</el-checkbox>
          <el-checkbox label="4">人员介绍</el-checkbox>
          <el-checkbox label="5">个别交谈</el-checkbox>
          <el-checkbox label="6">亲临实践</el-checkbox>
          <el-checkbox label="7">会议</el-checkbox>
          <el-checkbox label="8">图片、照片</el-checkbox>
          <el-checkbox label="9">书报刊物</el-checkbox>
          <el-checkbox label="10">统计报表</el-checkbox>
          <el-checkbox label="11">影视资料</el-checkbox>
          <el-checkbox label="12">文件</el-checkbox>
          <el-checkbox label="13">集体组织</el-checkbox>
          <el-checkbox label="14">自发</el-checkbox>
          <el-checkbox label="15">其他</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <br />
      <el-form-item
        v-for="(cooperate, index) in ruleForm.cooperates"
        :label="cooperatesName[index]"
        :key="cooperate.key"
        label-width="100px"
      >
        <el-form-item
          label="姓名"
          :prop="'cooperates.' + index + '.name'"
          :rules="{
              required: true, message: '姓名不能为空', trigger: 'blur'
            }"
        >
          <el-input v-model="cooperate.name" class="smallInput" :disabled="limit"></el-input>
        </el-form-item>
        <el-form-item
          label="学号"
          :prop="'cooperates.' + index + '.student_id'"
          :rules="{
              required: true, message: '学号不能为空', trigger: 'blur'
            }"
        >
          <el-input v-model="cooperate.student_id" class="smallInput" :disabled="limit"></el-input>
        </el-form-item>
        <el-form-item
          label="现学历"
          :prop="'cooperates.' + index + '.education_background'"
          :rules="{
              required: true, message: '请选择学历', trigger: 'change'
            }"
        >
          <el-select
            v-model="cooperate.education_background"
            placeholder="请选择学历"
            class="smallInput"
            :disabled="limit"
          >
            <el-option label="未选择" value="0"></el-option>
            <el-option label="A 大专" value="1"></el-option>
            <el-option label="B 大学本科" value="2"></el-option>
            <el-option label="C 硕士研究生" value="3"></el-option>
            <el-option label="D 博士研究生" value="4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="邮箱"
          :prop="'cooperates.' + index + '.email'"
          :rules="[
              { required: true, message: '请输入邮箱地址', trigger: 'blur' },
              { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
            ]"
        >
          <el-input v-model="cooperate.email" class="middleInput" :disabled="limit"></el-input>
        </el-form-item>
        <el-form-item
          label="联系电话"
          :prop="'cooperates.' + index + '.telephone'"
          :rules="{
              required: true, message: '请输入手机号码', trigger: 'blur'
            }"
        >
          <el-input v-model="cooperate.telephone" class="middleInput" :disabled="limit"></el-input>
        </el-form-item>
        <el-button @click.prevent="removeCooperate(cooperate)" :disabled="limit">删除</el-button>
      </el-form-item>
      <br />
      <el-form-item>
        <el-button @click="addCooperate" style="width:120px" :disabled="limit">新增合作者</el-button>
      </el-form-item>
      <br />
    </el-form>
    <el-row>
      <el-col :span="8" :offset="4" v-if="role=='student'">
        <el-button type="primary" @click="jump()">PDF预览</el-button>
      </el-col>
      <el-col :span="8" v-if="role!='student'">
        <div style="width:10px;height:10px"></div>
      </el-col>
      <el-col :span="8">
        <download :proid="id" :filename="ruleForm['name']"></download>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import api from "@/api/apis";
import download from "@/components/download.vue";
export default {
  props: { id: String, role: String },
  components: {
    download
  },
  data() {
    return {
      applyId: "",
      limit: true,
      projectState: 1,
      cooperatesName: ["第一合作者", "第二合作者", "第三合作者"],
      display_info: [
        "实物、产品",
        "模型",
        "图纸",
        "磁盘",
        "现场演示",
        "图片",
        "录像",
        "样品"
      ],
      ruleForm: {
        name: "",
        stuid: "",
        eduBackground: "0",
        major: "",
        date1: "",
        year: "",
        projectName: "",
        address: "",
        phone: "",
        email: "",
        projectClass: "0",
        descriptions: "",
        innovation: "",
        keywords: "",
        type: "0",
        display: [],
        investigate: [],
        cooperates: [
          {
            name: "",
            student_id: "",
            education_background: "0",
            telephone: "",
            email: ""
          }
        ]
      },
      rules: {
        name: [{ required: true, message: "请输入学生姓名", trigger: "blur" }],
        stuid: [{ required: true, message: "请输入学生学号", trigger: "blur" }],
        eduBackground: [
          { required: true, message: "请选择学历", trigger: "change" }
        ],
        major: [{ required: true, message: "请填写专业", trigger: "blur" }],
        projectName: [
          { required: true, message: "请填写作品名称", trigger: "blur" }
        ],
        phone: [{ required: true, message: "请填写手机号码", trigger: "blur" }],
        address: [
          { required: true, message: "请填写通讯地址", trigger: "blur" }
        ],
        descriptions: [
          { required: true, message: "请填写作品说明", trigger: "blur" }
        ],
        innovation: [
          { required: true, message: "请填写创新说明", trigger: "blur" }
        ],
        keywords: [
          { required: true, message: "请填写关键字", trigger: "blur" }
        ],
        display: [
          {
            type: "array",
            required: true,
            message: "请至少选择一种展示形式",
            trigger: "change"
          }
        ],
        investigate: [
          {
            type: "array",
            required: true,
            message: "请至少选择一种调查形式",
            trigger: "change"
          }
        ],
        type: [{ required: true, message: "请选择类别", trigger: "change" }],
        projectClass: [
          { required: true, message: "请选择分类", trigger: "change" }
        ],
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"]
          }
        ],
        date1: [
          {
            required: true,
            message: "请选择出生日期",
            trigger: "change"
          }
        ],
        year: [
          {
            required: true,
            message: "请选择入学时间",
            trigger: "blur"
          }
        ]
      }
    };
  },
  created: function() {
    //this.paperid="53e99784b7602d9701f3e132"
    var that = this;
    this.applyId = this.id;
    if (that.role == "admin") {
      api.administrator_get_project(this.applyId).then(function(e) {
        var res = JSON.parse(e.data.data);
        that.projectState = res["state"];
        that.limit = true;
        (that.ruleForm.name = res["name"]),
          (that.ruleForm.stuid = res["student"]),
          (that.ruleForm.eduBackground = res["education_background"]),
          (that.ruleForm.major = res["major"]),
          (that.ruleForm.date1 = res["birth_date"]);
        that.ruleForm.year = res["year"];
        that.ruleForm.address = res["address"];
        that.ruleForm.phone = res["telephone"];
        that.ruleForm.email = res["email"];
        that.ruleForm.projectName = res["full_name"];
        that.ruleForm.projectClass = res["category"];
        that.ruleForm.descriptions = res["descriptions"];
        that.ruleForm.innovation = res["innovation"];
        that.ruleForm.keywords = res["keywords"];
        that.ruleForm.type = res["type"];
        var d = eval(res["cooperator"]);
        var s = [];
        for (var i = 0; i < d.length; i++) {
          s.push(JSON.parse(d[i]));
        }
        that.ruleForm.cooperates = s;
        var d1 = eval(res["type_info"]);
        var s1 = [];
        for (var i1 = 0; i1 < d1.length; i1++) {
          s1.push(d1[i1]);
        }
        that.ruleForm.display = s1;
        that.ruleForm.investigate = s1;
      });
    } else if (that.role == "student") {
      api.student_get_project(this.applyId).then(function(e) {
        var res = JSON.parse(e.data.data);
        that.projectState = res["state"];
        if (
          (that.role == "student" && that.projectState == 1) ||
          (that.role == "student" && that.projectState == 2)
        ) {
          that.limit = true;
        } else if (that.role == "student" && that.projectState == 0) {
          that.limit = false;
        } else {
          that.limit = true;
          this.$message("error");
        }
        (that.ruleForm.name = res["name"]),
          (that.ruleForm.stuid = res["student"]),
          (that.ruleForm.eduBackground = res["education_background"]),
          (that.ruleForm.major = res["major"]),
          (that.ruleForm.date1 = res["birth_date"]);
        that.ruleForm.year = res["year"];
        that.ruleForm.address = res["address"];
        that.ruleForm.phone = res["telephone"];
        that.ruleForm.email = res["email"];
        that.ruleForm.projectName = res["full_name"];
        that.ruleForm.projectClass = res["category"];
        that.ruleForm.descriptions = res["descriptions"];
        that.ruleForm.innovation = res["innovation"];
        that.ruleForm.keywords = res["keywords"];
        that.ruleForm.type = res["type"];
        that.ruleForm.display = res["type_info"];
        that.ruleForm.investigate = res["type_info"];
        //处理cooperator 和 type_info
        var d = eval(res["cooperator"]);
        var s = [];
        for (var i = 0; i < d.length; i++) {
          s.push(JSON.parse(d[i]));
        }
        that.ruleForm.cooperates = s;
        var d1 = eval(res["type_info"]);
        var s1 = [];
        for (var i1 = 0; i1 < d1.length; i1++) {
          s1.push(d1[i1]);
        }
        that.ruleForm.display = s1;
        that.ruleForm.investigate = s1;
      });
    } else if (that.role == "expert") {
      api.expert_get_project(this.applyId).then(function(e) {
        var res = JSON.parse(e.data.data);
        that.projectState = res["state"];
        that.role = true;
        (that.ruleForm.name = res["name"]),
          (that.ruleForm.stuid = res["student"]),
          (that.ruleForm.eduBackground = res["education_background"]),
          (that.ruleForm.major = res["major"]),
          (that.ruleForm.date1 = res["birth_date"]);
        that.ruleForm.year = res["year"];
        that.ruleForm.address = res["address"];
        that.ruleForm.phone = res["telephone"];
        that.ruleForm.email = res["email"];
        that.ruleForm.projectName = res["full_name"];
        that.ruleForm.projectClass = res["category"];
        that.ruleForm.descriptions = res["descriptions"];
        that.ruleForm.innovation = res["innovation"];
        that.ruleForm.keywords = res["keywords"];
        that.ruleForm.type = res["type"];
        that.ruleForm.display = res["type_info"];
        that.ruleForm.investigate = res["type_info"];
        var d = eval(res["cooperator"]);
        var s = [];
        for (var i = 0; i < d.length; i++) {
          s.push(JSON.parse(d[i]));
        }
        that.ruleForm.cooperates = s;
        var d1 = eval(res["type_info"]);
        var s1 = [];
        for (var i1 = 0; i1 < d1.length; i1++) {
          s1.push(d1[i1]);
        }
        that.ruleForm.display = s1;
        that.ruleForm.investigate = s1;
      });
    }
  },
  methods: {
    jump() {
      this.stageInfo();
      this.$router.push({
        path: "/printfile",
        query: {
          id: this.applyId
        }
      });
    },
    save(func) {
      var that = this;
      var temp = {};
      var info = {};
      for (var i = 0; i < this.ruleForm.cooperates.length; i++) {
        temp[i] = JSON.stringify(this.ruleForm.cooperates[i]);
      }
      var typeinfo = {};
      if (that.ruleForm.type == "1") {
        typeinfo = JSON.stringify(this.ruleForm.display);
      } else if (that.ruleForm.type == "2") {
        typeinfo = JSON.stringify(this.ruleForm.investigate);
      } else if (that.ruleForm.type == "0") {
        typeinfo = JSON.stringify(this.ruleForm.investigate);
      }
      info = JSON.stringify({
        cooperator_info: temp,
        email: this.ruleForm.email,
        full_name: this.ruleForm.projectName,
        telephone: this.ruleForm.phone,
        address: this.ruleForm.address,
        innovation: this.ruleForm.innovation,
        keywords: this.ruleForm.keywords,
        category: this.ruleForm.projectClass,
        descriptions: this.ruleForm.descriptions,
        education_background: this.ruleForm.eduBackground,
        type: that.ruleForm.type,
        type_info: typeinfo
      });
      api.modify_application(that.applyId, info).then(func);
    },
    submitForm(formName) {
      var that = this;
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.ruleForm.eduBackground == "0") {
            this.$message("没填学历");
          } else if (this.ruleForm.projectClass == "0") {
            this.$message("没选分类");
          } else if (this.ruleForm.type == "0") {
            this.$message("没选类别");
          } else if (
            this.ruleForm.type == "1" &&
            this.ruleForm.display.length == 1
          ) {
            this.$message("没选展示方式");
          } else if (
            this.ruleForm.type == "2" &&
            this.ruleForm.investigate.length == 1
          ) {
            this.$message("没选调查方式");
          } else {
            this.save(function(res) {
              if (res["data"]["code"] == 200) {
                api.submit_application(that.applyId).then(function(res) {
                  if (res["data"]["code"] == 200) {
                    that.$message("提交成功!");
                    that.$router.push("/StuConList");
                  }
                });
              }
            });
          }
        } else {
          this.$message("提交失败!");
          return false;
        }
      });
    },
    stageInfo() {
      var that = this;
      this.save(function(res) {
        console.log(res);
        if (res["data"]["code"] == 200) {
          that.$message("保存成功");
          // that.$router.push("/StuConList");
        } else {
          that.$message("保存失败");
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    removeCooperate(item) {
      var index = this.ruleForm.cooperates.indexOf(item);
      if (index !== -1) {
        this.ruleForm.cooperates.splice(index, 1);
      }
    },
    addCooperate() {
      if (this.ruleForm.cooperates.length < 3) {
        this.ruleForm.cooperates.push({
          name: "",
          student_id: "",
          education_background: "0",
          telephone: "",
          email: "",
          key: Date.now()
        });
      } else {
        this.$message("合作者最多只能填写三人", "警告", {
          confirmButtonText: "确定"
        });
      }
    }
  }
};
</script>
<style scoped>
.smallInput {
  width: 100px;
}
.middleInput {
  width: 160px;
}
.Input {
  width: 500px;
}
</style>
