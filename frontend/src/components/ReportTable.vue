<template>
  <div class="report-wrapper">
    <h2 class="pb-3">
        Payroll Report
    </h2>
    <!-- data table -->
    <vue-good-table
      :columns="columns"
      :rows="rows"
      :sort-options="{
        enabled: true
      }"
      :search-options="{
        enabled: true,
        placeholder: 'Search by employee number',
        searchFn: searchEmployees,
      }"
    />
  </div>
</template>

<script>
import {VueGoodTable} from 'vue-good-table'

export default {
  name: 'ReportTable',
  components: {
    VueGoodTable
  },
  props: {
    rows: {
      default: () => [],
      type: Array
    }
  },
  methods: {
    searchEmployees (row, col, cellValue, searchTerm) {
      return row.employee === searchTerm
    },
    sortNumber (x, y) {
      return (x < y ? -1 : (x > y ? 1 : 0))
    },
    formatDollar (value) {
      return '$'+ value.toFixed(2)
    }
  },
  data () {
    return {
      columns: [
        {
          label: 'Employee ID',
          field: 'employee'
        },
        {
          label: 'Pay Period',
          field: 'pay_period',
          thClass: 'text-center',
          tdClass: 'text-center'
        },
        {
          label: 'Pay Amount',
          field: 'pay_amount',
          sortable: true,
          sortFn: this.sortNumber,
          formatFn: this.formatDollar,
          thClass: 'right-header',
          tdClass: 'text-right'
        }
      ]
    }
  }
}
</script>

<style lang="scss">
@import 'static/variables.scss';

// table style
.vgt-wrap {
  border-radius: $b-radius;
  overflow: hidden;
  .vgt-global-search, {
    background: $c-grey !important;
    padding: $margin 0;
  }
  .sorting {
    background: $c-grey !important;
    padding: $margin $margin;
  }
  .vgt-table th.sorting:after {
    border-bottom-color: $c-primary;
  }
  .vgt-table th.sorting:after {
    border-top-color: $c-primary;
  }
  tbody td {
    padding: $margin $margin;
  }
  tbody tr:nth-child(even) {
    background: rgba($c-primary, 0.03);
  }
  *:not(.magnifying-glass) {
    border: none !important;
    transition: all 0.25s ease !important;
  }
  // Right aligned header style that works with header
  .right-header {
    text-align: right;
    position: relative;
    span {
      position: absolute;
      display: block;
      width: 100%;
      height: 100%;
      right: $margin;
      top: calc(50% - 0.75em);
    }
    &:hover span {
      right: $margin*2;
    }
    &.sorting-desc, &.sorting-asc {
      span {
        right: $margin*2;
      }
    }
  }
}

</style>
