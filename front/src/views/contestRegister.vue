<template>
    <el-card class="applyInfoForm" shadow="always" style="opacity:0.6;margin: 0 auto; width:60%">
        <div slot="header">
            <span>注册竞赛</span>
        </div>
        <ContestRegister @submit="submit" :id="-1">
        </ContestRegister>
    </el-card>
</template>

<script>
import ContestRegister from '@/components/contestRegister.vue'
import api from "@/api/apis";
export default {
    components:{
        ContestRegister
    },
    methods:{
        submit:function(name,stopDate,enddate,description){
            var that=this;
            api.add_contest(name,description,enddate,stopDate).then(function(e){
                if(e["data"]["code"]==200){
                    that.$message("添加成功");
                    that.$router.push("/ContestList");
                }
            })
        }
    }
}
</script>
