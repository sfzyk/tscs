<template>
  <el-card style="width:90%;margin:0 auto">
    <el-row class="sprow">
      <ExpList ref="explist" @clickRow="clickRow" @pageChange="onCancel" />
    </el-row>
    <el-row class="sprow" v-show="isEdit">
      <el-card class="spcard">
        <el-form :inline="true" :model="addExp" ref="addExp" size="mini" :rules="rules">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="addExp.name" class="spforminput"></el-input>
          </el-form-item>
          <el-form-item label="专业" prop="field">
            <el-select v-model="addExp.field" class="spforminput">
              <el-option label="A.机械控制" value="0"></el-option>
              <el-option label="B.信息技术" value="1"></el-option>
              <el-option label="C.数理" value="2"></el-option>
              <el-option label="D.生命科学" value="3"></el-option>
              <el-option label="E.能源化工" value="4"></el-option>
              <el-option label="F.哲学社会科学" value="5"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="院系" prop="college">
            <el-input v-model="addExp.college" class="spforminput"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="addExp.email" class="spforminput"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="telephone">
            <el-input v-model.number="addExp.telephone" class="spforminput"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit('addExp')">添加</el-button>
          </el-form-item>
        </el-form>
        <el-row>
          <el-col :span="12">
            <el-button type="primary" @click="downloadForm" size="mini">下载模板</el-button>
          </el-col>
          <el-col :span="12">
            <el-upload
              class="upload-demo"
              action
              multiple
              :limit="num"
              :before-upload="beforeupload"
              :file-list="fileList"
              :accept="accepts"
              :on-change="change"
            >
              <el-tooltip content="请下载模板并填写后上传，即可批量导入评委" placement="bottom" effect="light">
                <el-button type="primary" size="mini">导入评委列表</el-button>
              </el-tooltip>
            </el-upload>
          </el-col>
        </el-row>
      </el-card>
    </el-row>
    <el-row class="sprow" v-show="isEdit&&isModified">
      <el-card class="spcard">
        <el-row>
          <el-form :inline="true" :model="modifyExp" ref="modifyExp" size="mini" :rules="rules">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="modifyExp.name" class="spforminput"></el-input>
            </el-form-item>
            <el-form-item label="领域" prop="field">
              <el-select v-model="modifyExp.field" class="spforminput">
                <el-option label="A.机械控制" value="0"></el-option>
                <el-option label="B.信息技术" value="1"></el-option>
                <el-option label="C.数理" value="2"></el-option>
                <el-option label="D.生命科学" value="3"></el-option>
                <el-option label="E.能源化工" value="4"></el-option>
                <el-option label="F.哲学社会科学" value="5"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="院系" prop="college">
              <el-input v-model="modifyExp.college" class="spforminput"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="modifyExp.email" class="spforminput" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="联系电话" prop="telephone">
              <el-input v-model.number="modifyExp.telephone" class="spforminput"></el-input>
            </el-form-item>
          </el-form>
        </el-row>
        <el-row type="flex" class="sprow1" justify="space-around">
          <el-col :span="3">
            <el-button type="primary" @click="onModify('modifyExp')">修改</el-button>
          </el-col>
          <el-col :span="3">
            <el-popover ref="popover" placement="top" width="160" v-model="visible">
              <p>确定删除吗？</p>
              <div style="text-align: right; margin: 0">
                <el-button size="mini" type="text" @click="visible = false">取消</el-button>
                <el-button type="primary" size="mini" @click="onDelete('modifyExp')">确定</el-button>
              </div>
            </el-popover>
            <el-button type="primary" v-popover:popover>删除</el-button>
          </el-col>
          <el-col :span="3">
            <el-button type="primary" @click="onCancel">取消</el-button>
          </el-col>
        </el-row>
      </el-card>
    </el-row>
    <el-row class="sprow">
      <el-button type="primary" @click="edit" v-show="!isEdit">编辑</el-button>
      <el-button type="primary" @click="back" v-show="isEdit">取消</el-button>
    </el-row>
  </el-card>
</template>

<script>
import api from "@/api/apis.js";
import ExpList from "@/components/ExpList.vue";
export default {
  components: {
    ExpList
  },
  data() {
    return {
      fileList: [],
      num: 1,
      accepts: ".xls,.xlsx",
      isEdit: false,
      isModified: false,
      visible: false,
      addExp: {
        name: "",
        field: "",
        college: "",
        email: "",
        telephone: ""
      },
      modifyExp: {
        name: "",
        field: "",
        college: "",
        email: "",
        telephone: "",
        expert_id: ""
      },
      rules: {
        name: [
          { required: true, message: "请输入评委名称", trigger: "change" }
        ],
        field: [
          { required: true, message: "请选择评委专业", trigger: "change" }
        ],
        college: [
          { required: true, message: "请输入评委院系", trigger: "change" }
        ],
        email: [
          { required: true, message: "请输入评委邮箱", trigger: "change" },
          { type: "email", message: "请输入正确的邮箱地址", trigger: "change" }
        ],
        telephone: [
          { required: true, message: "请输入评委联系电话", trigger: "change" },
          { type: "number", message: "电话必须为数字" }
        ]
      }
    };
  },
  methods: {
    edit() {
      this.isEdit = true;
    },
    back() {
      this.isEdit = false;
    },
    clickRow(val) {
      this.$refs["modifyExp"].resetFields();
      this.isModified = true;
      this.modifyExp.name = val.name;
      this.modifyExp.field = val.field;
      this.modifyExp.college = val.college;
      this.modifyExp.email = val.email;
      this.modifyExp.telephone = parseInt(val.telephone);
      this.modifyExp.expert_id = val.id;
    },
    onSubmit(formName) {
      var that = this;
      this.$refs[formName].validate(valid => {
        if (valid) {
          api.load_expert(that.addExp).then(function(result) {
            if (result["data"]["code"] === 200) {
              that.$refs.explist.reflshTable();
              that.addExp.name = "";
              that.addExp.field = "";
              that.addExp.college = "";
              that.addExp.email = "";
              that.addExp.telephone = "";
              that.$refs[formName].resetFields();
            } else if (result["data"]["code"] === 207) {
              that.$message("邮箱已存在！");
            }
          });
        } else {
          return false;
        }
      });
    },
    onModify(formName) {
      var that = this;
      this.$refs[formName].validate(valid => {
        if (valid) {
          api.modify_expert(that.modifyExp).then(function(result) {
            if (result["data"]["code"] === 200) {
              that.$refs.explist.reflshTable();
              that.$refs[formName].resetFields();
              that.onCancel();
            }
          });
        } else {
          return false;
        }
      });
    },
    onDelete(formName) {
      var that = this;
      api.delete_expert(this.modifyExp.expert_id).then(function(result) {
        if (result["data"]["code"] === 200) {
          that.$refs.explist.reflshTable();
          that.$refs[formName].resetFields();
          that.visible = false;
          that.onCancel();
        }
      });
    },
    onCancel() {
      this.$refs.explist.cancel();
      this.isModified = false;
    },
    downloadForm() {
      api.example_expertinfo();
    },
    change() {
      this.fileList = [];
    },

    request(req) {
      console.log(req);
    },
    progress(file, fileList) {},
    beforeupload(file) {
      var that = this;
      that.$message({
        message: "开始上传"
      });
      api.load_experts(file).then(function(result) {
        console.log(result);
        that.$refs.explist.reflshTable();
        that.$message({
          message: `上传成功！${result['data']['data']}个条目导入失败！`,
          type: "success"
        });
      });
    }
  }
};
</script>

<style>
.sprow {
  margin: 5vh;
}
.spcard {
  width: 100%;
  margin: 0 auto;
}
.spforminput {
  width: 25vh;
}
.sprow1 {
  margin: 0 auto;
  width: 60vh;
}
</style>