import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from "vue";
import axios from 'axios';

import App from './App.vue';
import router from './router';

const app = createApp(App);

axios.defaults.withCredentials = true;  // 允许跨域请求时携带凭证（如 cookies）
axios.defaults.baseURL = 'http://localhost:5000/';  // the FastAPI backend

app.use(router);
app.mount("#app");  // 将 Vue 应用实例挂载到 HTML 中 id 为 app 的元素上