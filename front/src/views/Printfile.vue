<template>
    <div class="back">
  <div class="row" id="pdfDom" style="padding-top: 55px;background-color:#fff; ">
      <h1>作品申报情况表</h1>
      <table border="1" class="tableForm" >
        <tr>
          <td rowspan="6" width="20">申报者情况</td>
          <td align="center" width="120">姓名</td>
          <td align="center" width="120">{{name}}</td>
          <td align="center" width="120">学号</td>
          <td align="center" width="120">{{stuid}}</td>
          <td align="center" width="120">出生年月</td>
          <td align="center" width="120">{{birth}}</td>
        </tr>
        <tr>
          <td align="center" width="120">现学历</td>
          <td align="center" colspan="5">{{degreearr[(degree)-0]}}</td>
        </tr>
        <tr>
          <td align="center">专业</td>
          <td align="center" colspan="3">{{major}}</td>
          <td align="center" width="120">入学时间</td>
          <td align="center" width="120">{{time}}</td>
        </tr>
        <tr>
          <td colspan="1">作品全称</td>
          <td colspan="5">{{full_name}}</td>
        </tr>
        <tr>
          <td rowspan="2">通讯地址</td>
          <td rowspan="2" colspan="3">{{address}}</td>
          <td>联系电话</td>
          <td>{{telephone}}</td>
        </tr>
        <tr>
          <td>邮箱</td>
          <td>{{email}}</td>
        </tr>
        <tr>
          <td height=200 align="center" rowspan="5">合作者情况</td>
          <td height =40 align="center" >姓名</td>
          <td align="center" >学号</td>
          <td align="center" >现学历</td>
          <td align="center" >联系电话</td>
          <td colspan="2" align="center" >邮箱</td>
        </tr>
        <tr v-for="item in cooperates" :key="item.name">     
          <td>{{item.name}} </td>
          <td>{{item.student_id}} </td>
          <td>{{degreearr[(item.education_background)-0]}}</td>
          <td>{{item.telephone}} </td>
          <td colspan="2">{{item.email}}</td>
        </tr>
        <tr>
            <td height = 50 colspan="2">作品名称</td>
            <td colspan="5">{{full_name}} </td>
        </tr>
        <tr>
            <td height = 70 colspan="2">作品分类</td>
            <td colspan="5">{{projectClassarr[projectClass-0]}} </td>
        </tr>
        <tr>
            <td height= 70 colspan="2">作品总体情况说明</td>
            <td colspan="5">{{descriptions}}</td>
        </tr>
        <tr>
            <td height=70  colspan="2">创新点</td>
            <td colspan="5"> {{innovation}}</td>
        </tr>
        <tr>
            <td height = 70 colspan="2">关键词</td>
            <td colspan="5">{{keywords}}</td>
        </tr>
        <tr v-if="type2=='1'">
            <td height=70 colspan="2">作品可展示的形式</td>
            <td colspan="5">{{ display}}</td>
        </tr>
        <tr v-if="type2=='2'">
            <td height=70 colspan="2">作品调查的方式</td>
            <td colspan="5">{{investigate}}</td>
        </tr>
      </table>
    </div>
    <div height=20></div>
    <el-button type="primary" class="btn btn-primary" v-on:click="getPdf()">导出PDF</el-button>
  </div>
</template>
    
<script>
import api from "@/api/apis";
export default {
    //props:{id:String},
    data() {
        return {
            type2:"1",
            htmlTitle:"科技项目申请表",
            applyId:"",
            name:"",
            address:"",
            stuid:"",
            birth:"",
            degree:"",
            major:"",
            time:"",
            full_name:"",
            telephone:"",
            email:"",
            projectClass: "0",
            descriptions: "",
            innovation: "",
            keywords: "",
            cooperates:[],
            degreearr:["","大专","大学本科","硕士研究生","博士研究生"],
            display:"",
            investigate:"",
            projectClassarr:["","机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）","信息技术（包括计算机、电信、通讯、电子等）","数理（包括数学、物理、地球与空间科学等）","D.生命科学(包括生物､农学､药学､医学､健康､卫生､食品等)","能源化工（包括能源、材料、石油、化学、化工、生态、环保等）","哲学社会科学（包括哲学、经济、社会、法律、教育、管理）"],
            displayarr:["","实物、产品","模型","图纸","磁盘","现场演示","图片","录像","样品"],
            investigatearr:["","走访","问卷","现场采访","人员介绍","个别交谈","亲临实践","会议","图片、照片","书报刊物","统计报表","影视资料","文件","集体组织","自发","其他"]
            // [
            // {
            //     name: "",
            //     student_id: "",
            //     education_background: "0",
            //     telephone: "",
            //     email: ""
            // }
            // ],
        }
    },
    created:function(){
        var that = this;
        this.applyId = this.$route.query.id;
        //console.log(this.applyId)
        api.student_get_project(this.applyId).then(function(e){
            var res = JSON.parse(e["data"]["data"]);
            console.log(that.applyId)
            console.log(res);
            console.log(res["name"]);
           // console.log(JSON.parse(res["cooperator"][0])['name'])
            that.name = res["name"];
            that.email=res["email"];
            that.address=res["address"];
            that.time=res["year"];
            that.telephone = res["telephone"]
            that.major = res["major"]
            that.birth=res["birth_date"]
            that.stuid=res["student"]
            that.full_name=res["full_name"];
            that.degree=res["education_background"]
            that.projectClass=res["category"]
            that.descriptions = res["descriptions"]
            that.innovation=res["innovation"]
            that.keywords = res["keywords"]
            that.type2=res["type"]
  
            // that.display=res["type_info"]
            // that.investigate=res["type_info"]
            if(that.type2=="1"){
              res["type_info"]=JSON.parse(res["type_info"])
                var len = res["type_info"].length
              for(var i = 1;i<len;i++){
                that.display = that.display+that.displayarr[res["type_info"][i]-0]+"\t\t\t";
              }
              console.log("type_info"+res["type_info"])
              console.log(that.display)
            }
            if(that.type2=="2"){
              res["type_info"]=JSON.parse(res["type_info"])
                var len = res["type_info"].length
              for(var i = 1;i<len;i++){
                that.investigate = that.investigate+that.investigatearr[res["type_info"][i]-0]+"\t\t\t";
              }
              
              console.log("inves 3"+that.investigatearr[3])
              console.log("type_info1111"+res["type_info"])
            }
            // that.cooperates = res["cooperator"]

            var cp = res["cooperator"]
            var len = cp.length
            console.log(len)
            for(var i=0; i<len;i++)
            {
              that.cooperates.push(JSON.parse(cp[i]))
            }
            for(var i=0;i<4-len;i++){
              that.cooperates.push({name:"-"})
            }
        })

    },
};
</script>
<style lang="scss" scoped>
.back{
    margin: 30px auto 0px auto;
    width: 65%;
}
.tableForm {
  margin: 30px auto 40px auto;
    border-collapse: collapse;
}
.h2 {
  margin: 0 auto;
  text-align: center;
}
.table {
  border-collapse: collapse;
  text-align: center;
  margin: 0 auto;
}
.table span {
  display: inline-block;
  width: 100px;
  text-align: right;
}
</style>