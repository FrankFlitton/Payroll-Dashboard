<template>
  <b-container class="mt-5">
    <b-row>
      <b-col>
      dashboard layout here. <br>{{msg}} <br> {{res}}
      </b-col>
      <b-col>
      <transition name="fade">
        <div v-if="showTable">TABLE
          <vue-good-table
            :columns="columns"
            :rows="timeSheets"
            :sort-options="{
              enabled: true,
              initialSortBy: {
                field: 'pay_period',
                type: 'asc'
              }
            }"
            :search-options="{
              enabled: true,
              placeholder: 'Search this table',
            }"
          />
        </div>
        <b-form v-if="!showTable">
          <input type="file" @change="updateFile($event)" />
          <b-btn
            @click="handleSubmit()"
          >
            send!
          </b-btn>
        </b-form>
      </transition>

      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import HTTP from '@/http'
import _ from 'lodash'
import moment from 'moment'
import {VueGoodTable} from 'vue-good-table'

export default {
  name: 'PayrollDashboard',
  components: {
    VueGoodTable
  },
  mounted () {
    this.getTimeSheets()
  },
  computed: {
    showTable () {
      return !!this.timeSheets.length
    }
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
        .then(response => {
          vm.getTimeSheets()
        })
        .catch(error => {
          console.log(error)
        })
    },
    getTimeSheets () {
      let vm = this
      HTTP.get('/timesheet/')
        .then(response => {
          vm.timeSheets = vm.setupTimeSheets(response.data)
          console.log(vm.timeSheets)
        })
        .catch(error => {
          console.log(error)
        })
    },
    // Format the object for table viz
    setupTimeSheets (timeSheets) {
      let consolodatedTimeSheets = this.consolodateTimeSheets(timeSheets)

      console.log(consolodatedTimeSheets)

      return timeSheets.map(sheet => {
        sheet.employee = sheet.employee.id
        sheet.compensation = sheet.job_group.compensation.toString()
        sheet.pay_amount = sheet.job_group.compensation * sheet.hours_worked
        sheet.pay_date = moment(sheet.pay_date).format('LL')
        sheet.report = sheet.report.id
        return sheet
      })
    },
    consolodateTimeSheets (timeSheets) {
      return timeSheets
    }
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      res: '',
      timeSheets: [],
      columns: [
        {
          label: 'Employee ID',
          field: 'employee'
        },
        {
          label: 'Pay Period',
          field: 'pay_period'
        },
        {
          label: 'Pay Amount',
          field: 'pay_amount',
          sortable: true,
          sortFn: (x, y) => {
            return (x < y ? -1 : (x > y ? 1 : 0))
          }
        }
      ],
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
