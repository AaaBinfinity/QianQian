// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import AirQualityCharts1m from '@/components/AirQualityCharts1Mon.vue';
import AirQualityCharts1h from '@/components/AirQualityCharts1h.vue';
import AirQualityCharts1d from '@/components/AirQualityCharts1d.vue';
import AirQualityCharts1w from '@/components/AirQualityCharts1w.vue';
import AirQualityCharts1Mon from '@/components/AirQualityCharts1Mon.vue';
import AirQualityCharts6Mon from '@/components/AirQualityCharts6Mon.vue';
import AirQualityCharts1y from '@/components/AirQualityCharts1y.vue';
import AirQualityChartsAll from '@/components/AirQualityChartsAll.vue';
import AirQualityData from '@/components/AirQualityData.vue';


const routes = [
    { path: '/1m', component: AirQualityCharts1m },
    { path: '/1h', component: AirQualityCharts1h },
    { path: '/1d', component: AirQualityCharts1d },
    { path: '/1w', component: AirQualityCharts1w },
    { path: '/1M', component: AirQualityCharts1Mon },
    { path: '/6M', component: AirQualityCharts6Mon },
    { path: '/1y', component: AirQualityCharts1y },
    { path: '/all', component: AirQualityChartsAll },
    { path: '/Data', component: AirQualityData },
    { path: '/', redirect: '/1m' }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;
