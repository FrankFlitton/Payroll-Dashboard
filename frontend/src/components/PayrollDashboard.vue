<template>
  <b-container class="mt-5">
    <b-row>
      <b-col>
      dashboard layout here. <br>{{msg}} <br> {{res}}
      </b-col>
      <b-col>
        <b-form>
          <input type="file" @change="updateFile($event)" />
          <b-btn
            @click="handleSubmit()"
          >
            send!
          </b-btn>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import HTTP from '@/http'
// import _ from 'lodash'

export default {
  name: 'PayrollDashboard',
  mounted () {
  },
  created () {
    this.postFile()
  },
  methods: {
    handleSubmit () {
      this.postFile()
    },
    updateFile (event) {
      this.form.formData.append('file', event.target.files[0])
      console.log(this.form.formData)
    },
    postFile () {
      let vm = this
      HTTP.post('/uploads/', vm.form.formData, vm.form.headers)
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
      res: '',
      form: {
        formData: new FormData(),
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    }
  }
}
</script>
