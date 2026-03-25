<template>
  <div class="app">
    <h1>{{ message }}</h1>
    <p>当前计数: {{ count }}</p>
    <p>双倍计数: {{ doubleCount }}</p>
    <button @click="increment">增加计数</button>
    <button @click="reset">重置计数</button>
    <div class="card">
      <h2>用户信息</h2>
      <p>姓名: {{ user.name }}</p>
      <p>年龄: {{ user.age }}</p>
      <button @click="updateUser">更新用户信息</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      message: '欢迎使用Vue 3!',
      count: 0,
      user: {
        name: '张三',
        age: 25
      }
    }
  },
  computed: {
    doubleCount() {
      return this.count * 2
    }
  },
  methods: {
    increment() {
      this.count++
    },
    reset() {
      this.count = 0
    },
    updateUser() {
      this.user.name = '李四'
      this.user.age = 30
    }
  },
  mounted() {
    console.log('Vue应用已挂载')
  }
}
</script>

<style scoped>
.app {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card {
  margin-top: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>