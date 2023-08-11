<template>
  <time
    :title="datetime"
    :datetime="datetime">{{ output }}</time>
</template>

<script>
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import {userTimezone, utcToZoned} from '@/js/shared/Util/datetime';

dayjs.extend(relativeTime);

export default {
  name: 'TimeAgo',
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
  },
  computed: {
    output() {
      return dayjs(utcToZoned(this.datetime, this.tz)).fromNow();
    },
  }
}
</script>
