<template>
  <el-button type="primary" @click="dl">下载作品</el-button>
</template>
<script>
import api from "@/api/apis";
export default {
  name: "download",
  props: {
    proid: String,
    filename: String
  },
  methods: {
    dl() {
      api.student_zip_file(parseInt(this.proid));
    }
  }
};
</script>
