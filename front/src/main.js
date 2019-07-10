import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import htmlToPdf from '@/components/utils/htmlToPdf'
Vue.use(htmlToPdf)
Vue.use(ElementUI)

Vue.config.productionTip = false
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

let dithat=new Vue();
router.beforeEach((to, from, next) => {   // 使用钩子函数对路由进行权限跳转
  if(to.matched.some( m => m.meta.auth)){
    if(store.state.isLog==true){
      next()
    }
    else{
      dithat.$message({
        message: '请先登录',
        type:'warning',
        center:true
      });
      next('/')
    }
  }
  else
  {
    next();
  }
})
