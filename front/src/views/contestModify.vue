<template>
    <el-card class="applyInfoForm" shadow="always" style="opacity:0.6;margin: 0 auto; width:60%">
        <div slot="header">
            <span>注册竞赛</span>
        </div>
        <ContestRegister @submit="submit" :id="id">
        </ContestRegister>
    </el-card>
</template>

<script>
import ContestRegister from '@/components/contestRegister.vue'
import api from "@/api/apis";
import router from '@/router.js';

export default {
    name:"ContestModify",
    components:{
        ContestRegister
    },
    data(){
        return{
            id:0
        }
    },
    created:function(){
      this.id=this.$route.query.id;
    },
    methods:{
        submit:function(name,stopDate,enddate,description){
            var that=this;
            var info;
            info={
                "contest_id": this.id,
                "name": name,
                "descriptions": description,
                "expire_date": enddate,
                "checkin_expire_date": stopDate,
            }
            api.modify_contest(info).then(function(e){
                if(e["data"]["code"]==200){
                    that.$message("修改");
                    that.$router.push("/ContestList");
                }
            })
        }
    }
}
</script>
