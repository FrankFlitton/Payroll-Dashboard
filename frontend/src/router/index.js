import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import PayrollDashboard from '@/components/PayrollDashboard'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'PayrollDashboard',
      component: PayrollDashboard
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
