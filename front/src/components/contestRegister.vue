<template>
    <div align="center" style="width:100%;" >
        <el-row>
            比赛名称：
            <el-input
                :clearable="true"
                placeholder="比赛名称"
                v-model="contestName"
                style="width:75%">
            </el-input>
        </el-row>
    <br/>
    <br/>
    <br/>
    <el-row>
        <el-col :span="5" align="right">
            报名截止日期：
        </el-col>
        <el-col :span="7" align="left">
            <el-date-picker
                v-model="stopDate"
                type="date"
                placeholder="报名截止日期"
                >
            </el-date-picker>
        </el-col>
        <el-col :span="5" align="right">
            初审结束日期：
        </el-col>
        <el-col :span="7" align="left">
            <el-date-picker
                v-model="endDate"
                type="date"
                placeholder="竞赛结束日期">
            </el-date-picker>
        </el-col>
    </el-row>
    <br/>
    <br/>
    <br/>
        描述：&nbsp; &nbsp; &nbsp; &nbsp;
        <el-input
            type="textarea"
            autosize
            placeholder="描述"
            v-model="description"
            style="width:76%">
        </el-input>
    <br/>
    <br/>
    <br/>
        <el-button type="success" @click="submit">提交</el-button>
        <el-button type="danger" @click="clear">清空</el-button>
    </div>
</template>

<script>
import api from "@/api/apis.js"
export default {
    name:"ContestRegister",
    props:{
        id:Number
    },
    data(){
        return {
            stopDate:"2019-07-06 00:00:00",
            endDate:"2019-07-06 00:00:00",
            contestName:"",
            description:""
        }
    },
    methods:{
        clear:function(){
            var that;
            that=this;
            this.$alert(
                "确认清空？",
                "警告",
                {
                    confirmButtonText: '确定',
                    callback: action => {
                        if(action=="confirm"){
                            that.stopDate="2019-07-06 00:00:00";
                            that.endDate="2019-07-06 00:00:00";
                            that.contestName="";
                            that.description="";
                        }
                    }

                }
            )
        },
        submit:function(){
            this.$emit("submit",this.contestName,this.stopDate,this.endDate,this.description);
        }
    },
    created:function(){
        var that=this;
        if(this.id!=-1){
            api.get_contest_info(this.id).then(function(e){
                console.log(e);
                var result=JSON.parse(e["data"]["data"]["contest_info"]);
                that.contestName=result["name"];
                that.description=result["descriptions"];
                that.endDate=result["expire_date"];
                that.stopDate=result["checkin_expire_date"];
            })
        }
    }
}
</script>
