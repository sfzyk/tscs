import Vue from 'vue'
import Router from 'vue-router'
import ApplyInfo from './components/ApplyInfo.vue'
import Login from './views/Login.vue'
import Allproject from './views/Allproject.vue'
import Stuproject from './views/Stuproject.vue'
import UserInfo from './views/UserInfo.vue'
import Homepage from './views/Homepage.vue'
import ContestList from './components/ContestList.vue'
import StuApplyInfo from './views/stuApplyInfo.vue'
import ExpertApplyInfo from './views/expertApplyInfo.vue'
import Invitation from './views/Invitation.vue'
import Resetpasswd from './views/Resetpasswd.vue'
import ManageExp from './views/ManageExp.vue'
import AdminApplyInfo from './views/adminApplyInfo.vue'
import ContestRegister from './views/contestRegister.vue'
import Printfile from './views/Printfile.vue'
import ContestInfo from './components/ContestInfo.vue'
import Notice from './views/Notice.vue'
import ContestModify from "./views/contestModify.vue"
import ContestAssemble from './views/ContestAssemble.vue'
import AdminExpertList from './components/adminExpertlist.vue'
import ExpertInfo from './views/ExpertInfo.vue'
import StuConList from './components/StuConList.vue'
import noticeinfo from './views/noticeInfo'
import Expproject from './views/Expproject'
import FinalSelect from './views/finalSelect'
import config from './views/config'
Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login,
    },
    {
      path:'/noticeinfo',
      name:"noticeinfo",
      component:noticeinfo,
    },
    {
      path:'/printfile',
      name:'printfile',
      component:Printfile
    },
    {
      path:'/notice',
      name:'notice',
      component:Notice
    },
    {
      path:'/StuConList',
      name:'StuConList',
      component:StuConList,
      meta:{auth:true}
    },
    {
      path:'/invitation/*',
      name:"invitation",
      component:Invitation
    },
    {
      path:'/resetpasswd',
      name:"resetpasswd",
      component:Resetpasswd
    },
    {
      path: '/ContestList',
      name: 'ContestList',
      component: ContestList
    },
    {
      path:"/ContestModify",
      name:"ContestModefy",
      component:ContestModify
    },
    {
      path: '/ContestAssemble',
      name: 'ContestAssemble',
      component: ContestAssemble
    },
    {
      path: '/UserInfo',
      name: 'UserInfo',
      component: UserInfo,
      meta:{auth:true}
    },
    {
      path: '/applyInfo',
      name: 'applyInfo',
      component: ApplyInfo,
      meta:{auth:true}
    },
    {
      path: '/Homepage',
      name: 'homepage',
      component: Homepage,
    },
    {
      path: '/ContestInfo',
      name: 'ContestInfo',
      component: ContestInfo,
    },
    {
      path: '/contestRegister',
      name: 'contestregister',
      component: ContestRegister,
    },
    {
      path: '/allproject',
      name: 'allproject',
      component: Allproject,
    },
    {
      path: '/Stuproject',
      name: 'Stuproject',
      component: Stuproject,
      meta:{auth:true}
    },
    {
      path: '/StuApplyInfo',
      name: 'StuApplyInfo',
      component: StuApplyInfo,
    },
    {
      path: '/ManageExp',
      name: 'manageexp',
      component: ManageExp,
    },
    {
      path: '/AdminApplyInfo',
      name: 'AdminApplyInfo',
      component: AdminApplyInfo,
    },
    {
      path: '/ExpertApplyInfo',
      name: 'ExpertApplyInfo',
      component: ExpertApplyInfo,
    },
    {
      path: '/AdminExpertList',
      name: 'AdminExpertList',
      component: AdminExpertList,
    },
    {
      path: '/ExpertInfo',
      name: 'ExpertInfo',
      component: ExpertInfo,
    },
    {
      path: '/Expproject',
      name: 'Expproject',
      component: Expproject,
    },
    {
      path: '/FinalSelect',
      name: 'FinalSelect',
      component: FinalSelect,
    },
    {
      path: '/config',
      name: 'config',
      component: config,
    }
  ]
})
