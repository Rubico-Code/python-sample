<template>
  <div>
    <div class="form-group">
      <label>Address autocomplete</label>
      <input
        id="map-autocomplete-input"
        type="text"
        autocomplete="false"
        class="form-control"
        placeholder="Street address or City or Zip"
        name="location">
    </div>

    <section>
      <label>Location on map</label>
      <div
        ref="canvas"
        class="w-100 shadow-sm"
        style="height: 380px"/>
      <slot name="error"/>
    </section>
  </div>
</template>

<script>
import {Loader} from '@googlemaps/js-api-loader';
/* global google */

const defaultCenter = {
  latitude: 42.3505391,
  longitude: -71.0583728
};

export default {
  name: 'GoogleMapLocation',
  props: {
    initial: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      loader: null,
      /**
       * @type {google.maps.Map}
       */
      map: null,
      autocomplete: null,
      searchInput: null,
      params: this.initial,
    }
  },
  created() {
    this.loader = new Loader({
      apiKey: process.env.GOOGLE_MAP_API_KEY,
      version: 'quarterly',
      libraries: ['places']
    });
  },
  mounted() {
    this.init();
    this.searchInput = document.querySelector('#map-autocomplete-input');
  },
  methods: {
    init() {
      this.loader
        .load()
        .then(this.loadMap)
        .catch(error => {
          console.error(error)
          this.$toast.error('Unable to load Google map.<br>Refresh the page and try again.', {
            duration: 10000
          });
        });
    },
    loadMap() {
      const {latitude, longitude} = (this.params.latitude && this.params.longitude) ? this.params : defaultCenter;
      const mapCenter = new google.maps.LatLng(latitude, longitude);

      this.map = new google.maps.Map(this.$refs.canvas, {
        zoomControl: true,
        zoomControlOptions: {
          position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        mapTypeControl: true,
        streetViewControl: false,
        scrollwheel: false,
        zoom: 12,
        fullscreenControl: true,
        fullscreenControlOptions: {
          position: google.maps.ControlPosition.RIGHT_TOP
        },
        mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        gestureHandling: 'auto',
      });
      this.map.setCenter(mapCenter);
      this.attachEventsToMap();
      this.marker = this.createMarker(mapCenter);
      this.attachEventsToMarker();
      this.attachSearch();
      this.searchInput.addEventListener('keydown', this.preventFormSubmission.bind(this))
      this.$emit('loaded')
    },
    createMarker(position) {
      return new google.maps.Marker({
        draggable: true,
        position: position,
        map: this.map,
        title: 'Drag me',
      });
    },
    attachSearch() {
      this.autocomplete = new google.maps.places.Autocomplete(this.searchInput, {
        types: ['establishment'],
        fields: ['name', 'formatted_address', 'geometry', 'address_component'],
        componentRestrictions: {
          country: 'us',
        },
      });

      this.autocomplete.addListener('place_changed', this.onPlaceChanged.bind(this));
    },
    onPlaceChanged() {
      const place = this.autocomplete.getPlace();
      console.log({place})

      if (!place.geometry) {
        console.error('Failed to retrieve address from Google.')
        return
      }

      this.$emit('placeChanged', place)

      const location = place.geometry.location
      this.map.panTo(location);
      this.map.setZoom(17);
      this.marker.setPosition(location);

      this.params.latitude = location.lat();
      this.params.longitude = location.lng();
    },
    preventFormSubmission(event) {
      if (event.keyCode === 13 || event.which === 13) {
        event.preventDefault();
        event.stopPropagation();
        return false;
      }
    },
    attachEventsToMap() {
      google.maps.event.addListener(this.map, 'idle', () => {
        google.maps.event.trigger(this.map, 'resize');
      });
    },
    attachEventsToMarker() {
      google.maps.event.addListener(this.marker, 'dragend', (event) => {
        this.params.latitude = event.latLng.lat();
        this.params.longitude = event.latLng.lng();
      });
    },
  },
  beforeDestroy() {
    [this.marker, this.autocomplete].map((item) => {
      google.maps.event.clearInstanceListeners(item);
    })
  }
}
</script>
