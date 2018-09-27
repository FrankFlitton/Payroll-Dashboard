<template>
  <b-container>
    <b-row>
      <b-col>
      dashboard layout here. <br>{{msg}} <br> {{res}}
      </b-col>
      <b-col>
        <b-form>
          <input type="file" @change="processFile($event)" />
          <b-btn>
            send!
          </b-btn>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import HTTP from '@/http'
import _ from 'lodash'

export default {
  name: 'PayrollDashboard',
  mounted () {
  },
  created () {
  },
  methods: {
    handleSubmit () {
      this.postFile()
    },
    postFile () {
      let vm = this
      let config = this.config
      HTTP.post('/', config)
        .then(function (response) {
          console.log(response)
          vm.res = response
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      res: ''
    }
  }
}
</script>
