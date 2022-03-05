<script>
import Plot from './Plotly.vue'

export default {
    props: ['wells', 'wellData', 'modelInfo'],
    data() {
        return {
            selectedWells: [],
            predictionResults: [],
            startDate: undefined,
            endDate: undefined
        }
    },
    methods: {
        createPlotlyLayout(well) {

            let d = this.wellData[well];
            let names = ['Oil production', 'Steam injection', 'Pressure', 'Water production'];
            let yVals = [d.oilProd, d.steamInj, d.pressure, d.waterProd];
            let visible = ['true', 'true', 'legendonly', 'legendonly'];
            let traces = [];


            yVals.forEach((elm, idx) =>
                traces.push(
                    {
                        x: d.date,
                        y: elm,
                        mode: 'lines',
                        type: 'scatter',
                        name: names[idx],
                        visible: visible[idx]
                    }
                )
            )

            let layout = {
                title: 'Production data for ' + well,
            }

            return { traces: traces, layout: layout }

        },
        // @FIXME: may want to limit the max size of the prediction results.
        async predictSelection() {
        }
    },
    computed: {
        dateBounds() {
            let results = {lower: undefined, upper: undefined}
            console.log(this.modelInfo)
            if (this.modelInfo === undefined || this.selectedWells.length === 0) {
                return results
            }

            let d = this.wellData;
            this.selectedWells.forEach(
                function (key) {
                    let dateArray = d[key].date;

                    if (dateArray.length != 0) {
                        let l = new Date(dateArray[0]);
                        let u = new Date(dateArray[dateArray.length - 1]);

                        if (l < results.lower || results.lower === undefined) {
                            results.lower = l;
                        }

                        if (results.upper > u || results.upper === undefined) {
                            results.upper = u;
                        }
                    }
                }
            )
            console.log(results.lower.toISOString())

            results.lower.setDate(results.lower.getDate() + this.modelInfo.inputChunkLength - 1)
            results.upper.setDate(results.upper.getDate() - this.modelInfo.outputChunkLength + 1)

            let resultsAsStrings = {
                lower: results.lower.toISOString().split('T')[0],
                upper: results.upper.toISOString().split('T')[0]
            }

            console.log(resultsAsStrings);
            return resultsAsStrings;
            
        },
    },
    watch: {
    },
    components: {
        Plot
    },
    created() {
    }
}
</script>

<template>
    <div>
        <select multiple v-model="selectedWells">
            <option v-for="well in wells" :key="well">{{ well }}</option>
        </select>

        <input type="date" id="start-date" v-bind:min="dateBounds.lower" />
        <div v-for="sel in selectedWells" :key="sel">
            <Plot :plot="createPlotlyLayout(sel)" />
        </div>
    </div>
</template>