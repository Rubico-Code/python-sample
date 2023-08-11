<template>
  <input
    type="tel"
    class="form-control"
    :placeholder="this.mask"
    v-maska:[options]
    :value="maskedValue"
    @maska="onMaska"
  >
</template>
<script>
import {vMaska} from 'maska';

export default {
  directives: {
    maska: vMaska
  },
  props: {
    value: {
      default: null,
      required: true,
      validator(value) {
        return value === null || typeof value === 'string' || value instanceof String || typeof value === 'number'
      }
    },
    mask: {
      type: String,
      default: '(###) ###-####'
    },
  },
  data() {
    return {
      options: {
        mask: this.mask,
      },
      maskedValue: null,
      prefix: '+1',
    }
  },
  created() {
    this.$watch('value', this.onChange, {
      immediate: true
    });
  },
  methods: {
    onMaska(event) {
      this.$emit('input', this.getModel(event.detail.unmasked));
    },
    onChange(newValue) {
      this.maskedValue = this.removePrefix(newValue) || '';
    },
    getModel(rawValue) {
      if (rawValue) {
        return this.prefix + rawValue;
      }

      return rawValue || null
    },
    removePrefix(value) {
      return value?.replace(this.prefix, '')
    }
  }
}
</script>
