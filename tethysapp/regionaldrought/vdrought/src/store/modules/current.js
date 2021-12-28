import {createStore} from "vuex";
import {getSlice, PostCurrentChartData} from '../api/current';

export default createStore({
    state() {
        return {
            basin: '',
            indices: 'Tair_f_tavg',
            periodicity: 'monthly',
            year: new Date().getFullYear() - 1
        };
    },
    mutations: {
        setBasin(state, payload) {
            state.basin = payload;
        },
        setIndices(state, payload) {
            state.indices = payload;
        },
        setPeriodicity(state, payload) {
            state.periodicity = payload;
        },
        setYear(state, payload) {
            state.year = payload;
        },
    },
    actions: {
        async SlicingThreddsCatalog(context, param) {
            let data=await getSlice(param);
            return data;
        },async ChartDataCurrent(context, param) {
            let data=await PostCurrentChartData(param);
            return data;
        },
    },
    modules: {},
});