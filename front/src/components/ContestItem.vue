<template>
  <div style="width: 100%; height:100%; margin: 0px;padding: 0px;">
    <div v-if="Ctype==-1" class="Contest" style="height:200px;"></div>

    <el-card v-if="Ctype==0" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_0">创</div>
          </el-col>
          <el-col :span="20">
            <router-link :to="{ path:'/ContestAssemble', query: { id: Cid ,priority: priority}}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="1">
            <router-link :to="{ path:'/contestModify', query: { id: Cid }}">
              <i class="el-icon-edit-outline"></i>
            </router-link>
          </el-col>
          <el-col :span="1">
            <i class="el-icon-delete" @click="DelContest()"></i>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card v-if="Ctype==1" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_1">报</div>
          </el-col>
          <el-col :span="18">
            <router-link :to="{ path:'/ContestAssemble', query: { id: Cid,priority: priority}}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" plain @click="dlall" v-if="priority==2">下载全部</el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card v-if="Ctype==2" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_2">审</div>
          </el-col>
          <el-col :span="18">
            <router-link :to="{ path:'/ContestAssemble', query: { id: Cid,priority: priority}}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" plain @click="dlall"  v-if="priority==2">下载全部</el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card v-if="Ctype==3" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_3">评</div>
          </el-col>
          <el-col :span="18">
            <router-link :to="{ path:'/ContestAssemble', query: { id: Cid ,priority: priority}}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" plain @click="dlall" v-if="priority==2">下载全部</el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card v-if="Ctype==4" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_4">选</div>
          </el-col>
          <el-col :span="18" v-if="priority==2">
            <router-link :to="{ path:'/FinalSelect', query: { contest_id: Cid }}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="18" v-if="priority==0">
            <router-link
              :to="{ path:'/ContestAssemble', query: { contest_id: Cid ,priority: priority}}"
            >
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" plain @click="dlall" v-if="priority==2">下载全部</el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card v-if="Ctype==5" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_5">终</div>
          </el-col>
          <el-col :span="18">
            <router-link :to="{ path:'/ContestAssemble', query: { id: Cid ,priority: priority}}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" plain @click="dlall" v-if="priority==2">下载全部</el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card v-if="Ctype==6" class="Contest" body-style="height:120px; padding:0px;" shadow="hover">
      <div slot="header">
        <el-row :gutter="10" style="line-height: 40px;">
          <el-col :span="2">
            <div class="StateIcon_6">史</div>
          </el-col>
          <el-col :span="18">
            <router-link :to="{ path:'/ContestAssemble', query: { id: Cid ,priority: priority}}">
              <div class="ContestTitle">{{name}}</div>
            </router-link>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" plain @click="dlall" v-if="priority==2">下载全部</el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row class="OuterRow">
          <el-col :span="12" class="LeftCol">
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">报名截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{checkin_end}}</el-col>
            </el-row>
            <el-row class="ContestLine">
              <el-col :span="10" class="LineTitle">初评截止时间：</el-col>
              <el-col :span="14" class="LineBody">{{end}}</el-col>
            </el-row>
          </el-col>
          <el-col :span="12" class="RightCol">
            <el-row class="RightRowTop">
              <el-col :span="24">描述:</el-col>
            </el-row>
            <el-row class="RightRowBottom">
              <el-col :span="24">{{description}}</el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import api from "@/api/apis.js";
import router from "@/router.js";
export default {
  name: "ContestItem",
  props: {
    priority: {
      type: Number,
      required: true
    },
    Cid: {
      type: Number,
      required: true
    },
    Ctype: {
      type: Number,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    checkin_end: {
      type: String,
      required: true
    },
    end: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  },
  methods: {
    DelContest: function() {
      var that = this;
      api.delete_contest(that.Cid).then(function(e) {
        console.log(e);
        if (e["data"]["code"] == 200) {
          that.$message({
            message: "删除成功"
          });
          that.$emit("DelEvent");
        }
      });
    },
    dlall() {
      api.admin_zip_file(this.Cid);
    }
  }
};
</script>

<style scoped>
.Contest {
  width: auto;
  margin: 20px 50px;
}
.ContestTitle {
  width: 100%;
  text-align: left;
  font-family: "微软雅黑";
}
.ContestLine {
  height: 60px;
  line-height: 60px;
}
.LineTitle {
  text-align: right;
}
.LineBody {
  text-align: center;
}
.OuterRow {
  height: 120px;
}
.RightCol {
  padding: 5px;
}
.RightRowTop {
  height: 40px;
  line-height: 40px;
  text-align: left;
}
.RightRowBottom {
  height: 70px;
  line-height: 35px;
  text-align: left;
  word-break: break-all;
  word-wrap: break-word;
  overflow: hidden;
  text-overflow: ellipsis;
}
.StateIcon_0 {
  border: 3px solid #ffaf1a;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
.StateIcon_1 {
  border: 3px solid #87ff26;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
.StateIcon_2 {
  border: 3px solid #ff80db;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
.StateIcon_3 {
  border: 3px solid #1af5ff;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
.StateIcon_4 {
  border: 3px solid #ffd17c;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
.StateIcon_5 {
  border: 3px solid #ff0e15;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
.StateIcon_6 {
  border: 3px solid #c4bebd;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  text-align: center;
  line-height: 35px;
}
</style>
