<template>
  <transition name="popup-slide">
    <div v-if="visible" class="achievement-popup">
      <img :src="icon" alt="Achievement Icon" class="popup-icon" />
      <div class="popup-content">
        <h4>{{ title }}</h4>
        <p>{{ description }}</p>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    icon: { type: String, required: true },
    title: { type: String, required: true },
    description: { type: String, required: true },
  },
  data() {
    return {
      visible: false,
    };
  },
  methods: {
    showPopup() {
      this.visible = true;
      setTimeout(() => {
        this.visible = false;
      }, 5000); // 5초 후 자동 닫힘
    },
  },
};
</script>

<style scoped>
.achievement-popup {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 300px;
  background-color: #2c3e50;
  color: white;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s;
}
.popup-icon {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}
.popup-content h4 {
  margin: 0;
  font-size: 16px;
}
.popup-content p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #bdc3c7;
}
/* Transition */
.popup-slide-enter-active,
.popup-slide-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
}
.popup-slide-enter {
  transform: translateY(100%);
  opacity: 0;
}
.popup-slide-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
