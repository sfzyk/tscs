<template>
  <div>
    <el-card style="width:80%;margin:0 auto 20px auto;opacity:0.6">
      <el-container>
        <el-header></el-header>
        <el-container>
          <el-aside width="350px">
            <MessageTable />
          </el-aside>
          <el-main>
            <el-row>
              <el-col :span="2">
                <div style="width:1px;height:350px;background-color:blue"></div>
              </el-col>
              <el-col :span="20">
                <Carousel />
              </el-col>
            </el-row>
          </el-main>
        </el-container>
      </el-container>
    </el-card>
  </div>
</template>

<script>
import Carousel from "@/components/Carousel.vue";
import MessageTable from "@/components/MessageTable.vue";
export default {
  name: "homepage",
  components: {
    Carousel,
    MessageTable
  },
  data() {
    return {};
  }
};
</script>