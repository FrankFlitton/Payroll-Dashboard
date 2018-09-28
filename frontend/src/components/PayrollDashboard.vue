<template>
  <b-container class="mt-5 mb-5">
    <b-row>
      <b-col>
      <transition name="fade">
        <div v-if="showTable">
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
      // Set up the data to process
      timeSheets.map(sheet => {
        sheet.employee = sheet.employee.id
        sheet.compensation = sheet.job_group.compensation
        sheet.pay_amount = sheet.job_group.compensation * sheet.hours_worked
        return sheet
      })
      let consolodatedTimeSheets = this.consolodateTimeSheets(timeSheets)

      return consolodatedTimeSheets
    },
    consolodateTimeSheets (timeSheets) {
      let compiledSheet = []
      // Seperate by payPeriod
      let payPeriods = _.groupBy(timeSheets, 'pay_period')
      payPeriods = _.forEach(payPeriods, (value, key) => {
        let activePeriod = key

        // Seperate by Employee Id
        payPeriods[key] = _.groupBy(payPeriods[key], 'employee')

        // Pack timesheet per employee per paydate
        for (let i in payPeriods[key]) {
          let tempObj = {}
          tempObj.pay_amount = 0
          tempObj.pay_period = activePeriod
          tempObj.employee = i

          // Sum total pay
          _.forEach(payPeriods[key][i], value => {
            tempObj.pay_amount += value.pay_amount
          })

          compiledSheet.push(tempObj)
        }
      })

      return compiledSheet
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
