<template>
  <b-tab title="Campaigns">
    <section class="card mb-3 border-top-0">
      <div class="card-body">
        <form
          id="campaign-export-form"
          @submit.prevent="submit">
          <div class="form-group form-row">
            <div class="col-md-3 required">
              <label class="small">Transaction Start date</label>
              <div class="input-group">
                <flat-pickr
                  id="input-start_datetime"
                  v-model="params.start_datetime"
                  :config="startConfig"
                  class="form-control"
                  placeholder="Start date"
                  name="start_datetime"
                  v-invalid="form.$errors"
                  @on-change="onStartChange"
                />
                <div class="input-group-append">
                  <button
                    v-show="!params.start_datetime"
                    class="btn btn-outline-secondary"
                    type="button"
                    title="Toggle"
                    data-toggle
                  >
                    <i class="fa fa-calendar-alt"/>
                  </button>
                  <button
                    v-show="params.start_datetime"
                    class="btn btn-outline-danger"
                    type="button"
                    title="Clear"
                    data-clear
                  >
                    <i class="fa fa-times"/>
                  </button>
                </div>
              </div>
              <field-error
                class="d-inline-block"
                :bag="form.$errors"
                field="start_datetime"/>
            </div>
            <div class="col-md-3 required">
              <label class="small">Transaction End date</label>
              <div class="input-group">
                <flat-pickr
                  id="input-end_datetime"
                  v-model="params.end_datetime"
                  :config="endConfig"
                  class="form-control"
                  placeholder="End date"
                  name="end_datetime"
                  v-invalid="form.$errors"
                  @on-change="onEndChange"
                />
                <div class="input-group-append">
                  <button
                    v-show="!params.end_datetime"
                    class="btn btn-outline-secondary"
                    type="button"
                    title="Toggle"
                    data-toggle
                  >
                    <i class="fa fa-calendar-alt"/>
                  </button>
                  <button
                    v-show="params.end_datetime"
                    class="btn btn-outline-danger"
                    type="button"
                    title="Clear"
                    data-clear
                  >
                    <i class="fa fa-times"/>
                  </button>
                </div>
              </div>
              <field-error
                class="d-inline-block"
                :bag="form.$errors"
                field="end_datetime"/>
            </div>
          </div>
          <div class="form-group">
            <label class="small">SalesRep (Multiselect)</label>
            <v-select
              placeholder="Name or email"
              @search="searchOwners"
              :options="adminOptions"
              label="searchLabel"
              multiple
              :deselect-from-dropdown="true"
              v-model="params.owners"
              :selectable="() => params.owners.length < 15"
            >
              <template #no-options="{ search, searching }">
                <template v-if="searching">
                  No results found for <em>{{ search }}</em>
                </template>
                <em
                  v-else
                  class="text-muted">Start typing to search</em>
              </template>
              <template #option="option">
                <span class="d-block">{{ $delve(option, 'profile.full_name', 'Unnamed') }}</span>
                <span class="small">{{ option.email }}</span>
              </template>
              <template #selected-option="user">
                {{ $delve(user, 'profile.full_name', user.email) }}
              </template>
            </v-select>
            <field-error
              class="d-inline-block"
              :bag="form.$errors"
              field="owners"/>
          </div>
        </form>
      </div>
      <div class="card-footer text-right">
        <button
          form="campaign-export-form"
          type="submit"
          class="btn btn-primary"
          :disabled="form.$pending">
          <i
            class="fas fa-fw fa-spin fa-sync-alt"
            v-if="form.$pending"
            aria-label="Loading"/>
          <i
            class="fas fa-fw fa-envelope"
            v-else/> Export
        </button>
      </div>
    </section>
  </b-tab>
</template>

<script>
import flatPickr from 'vue-flatpickr-component';
import Form from 'laravel-form-validation';
import {dateTimePickerConfig} from '@/js/shared/Util/flatpickr.js';
import {userTimezone} from '@/js/shared/Util/datetime.js';
import vSelect from 'vue-select'
import debounce from 'debounce';

export default {
  name: 'CampaignsTab',
  data: () => {
    return {
      params: {
        timezone: userTimezone(),
        owners: [],
        end_datetime: null
      },
      form: new Form(),
      startConfig: Object.assign({}, dateTimePickerConfig, {
        defaultHour: 0,
        defaultMinute: 0,
      }),
      endConfig: Object.assign({}, dateTimePickerConfig, {
        defaultHour: 23,
        defaultMinute: 59,
      }),
      admins: [],
    };
  },
  components: {
    flatPickr,
    vSelect,
  },
  methods: {
    submit() {
      this.form.post('/reports/campaigns', this.params)
        .then(() => {
          this.$toast.success('Request has been queued.<br>You will get an email soon.')
        })
    },
    onStartChange(selectedDates, dateStr) {
      this.$set(this.endConfig, 'minDate', dateStr);
    },
    onEndChange(selectedDates, dateStr) {
      this.$set(this.startConfig, 'maxDate', dateStr);
    },
    searchOwners: debounce(function (search, loading) {
      if (!search.length) {
        return;
      }

      loading(true);

      this.$http
        .get('/search/sales-reps', {
          params: {search},
        })
        .then((response) => {
          this.admins = response.data?.data || [];
        })
        .finally(() => {
          loading(false);
        });
    }, 300),
  },
  computed: {
    adminOptions() {
      return this.admins.map((user) => {
        user.searchLabel = user.email + ' ' + user.profile?.full_name;
        return user;
      })
    }
  }
}
</script>
