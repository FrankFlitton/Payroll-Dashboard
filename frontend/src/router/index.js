import Vue from 'vue'
import Router from 'vue-router'
import PayrollDashboard from '@/components/PayrollDashboard'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'PayrollDashboard',
      component: PayrollDashboard
    }
  ]
})
