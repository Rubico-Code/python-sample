<template>
  <time
    :title="datetime"
    :datetime="datetime">{{ output }}</time>
</template>

<script>
import {userTimezone, utcToZoned} from '@/js/shared/Util/datetime';

export default {
  name: 'DateTime',
  props: {
    datetime: {
      required: true,
      type: [String, Date]
    },
    tz: {
      type: String,
      required: false,
      default: () => userTimezone(),
    },
    format: {
      required: false,
      type: String,
      default: 'MM/DD/YY'
    },
    withTime: {
      required: false,
      type: Boolean,
      default: false,
    },
  },
  computed: {
    output() {
      return utcToZoned(this.datetime, this.tz, this.fullFormat)
    },
    fullFormat() {
      return this.withTime ? this.format + ', h:mm a' : this.format
    }
  },
}
</script>
