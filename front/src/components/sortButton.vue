<template>
    <el-button size="small" round @click="changeSort">{{appearance+" "+arrow}}</el-button>
</template>
<script>
export default {
    name:"sortButton",
    props:{
        appearance: String
    },
    data(){
        return{
            arrow:"-",
            sort:0
        }
    },
    methods:{
        clear(){
            this.sort=0;
            this.arrow="-";
        },
        changeSort(){
            this.sort=(this.sort+1)%3;
            this.$emit("change-sort",this.sort);
            if(this.sort===1){
                this.arrow='↓';
            }else if(this.sort===2){
                this.arrow='↑';
            }else if(this.sort===0){
                this.arrow='-';
            }else{
                this.sort=0;
            }
        }
    }
}
</script>
