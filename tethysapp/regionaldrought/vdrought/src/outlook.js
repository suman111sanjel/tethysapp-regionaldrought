import { createApp } from "vue";
import outlook from "./views/outlook.vue";
import store from "./store/modules/outlook";
import ElementPlus from "element-plus";

const app = createApp(outlook);
app.use(store);
app.use(ElementPlus);
app.mount('#app');