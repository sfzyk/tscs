<template>
  <div class="block" style="opacity:1">
    <span class="demonstration"></span>
    <el-carousel height="500px">
      <el-carousel-item v-for="item in url" :key="item">
        <h3 class="small">
          <el-image style="width: 720px; height: 405px" :src="item" :fit="fits"></el-image>
        </h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>
<script>
export default {
  data() {
    return {
      fits: "fill",
      url: [
        require("@/assets/1.jpg"),
        require("@/assets/2.jpg"),
        require("@/assets/3.jpg")
      ]
    };
  }
};
</script>
