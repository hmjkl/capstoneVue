<script>
import Plot from './Plotly.vue'

export default {
    props: ['wells', 'wellData', 'modelInfo'],
    data() {
        return {
            selectedWells: [],
            predictionResults: {},
            startDates: {},
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

            // Plot predictions if they exist...
            try {
                let selectedWellPrediction = this.predictionResults[well];
                traces.push(
                    {
                        x: selectedWellPrediction['dates'].map(e => new Date(e)),
                        y: selectedWellPrediction['oilProd'],
                        mode: 'lines',
                        type: 'scatter',
                        name: 'Predicted oil production'
                    }
                )
            } catch (err) {
            }

            let layout = {
                title: 'Production data for ' + well,
            }

            console.log(traces)

            return { traces: traces, layout: layout }

        },
        async predictSelection() {
            let selectedWellNames = this.selectedWells;
            let wellData = this.wellData;

            let send_obj = {
                wells: selectedWellNames,
                wellData: {},
            }

            for (let i = 0; i < selectedWellNames.length; i++) {
                let selectedWell = selectedWellNames[i];
                let selectedWellData = this.wellData[selectedWell];


                send_obj.wellData[selectedWell] = {
                    predictionDates: {
                        start: this.startDates[selectedWell],
                        end: this.endDate(selectedWell),
                    },
                    date: selectedWellData.date.map(e => this.dateAsString(e)),
                    oilProd: selectedWellData.oilProd,
                    steamInj: selectedWellData.steamInj,
                    pressure: selectedWellData.pressure,
                    waterProd: selectedWellData.waterProd
                }
            }

            console.log(send_obj)
            const url = 'http://localhost:5000/api/predict';
            fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(send_obj)
            })
                .then((data) => data.json())
                .then(obj => this.predictionResults = obj);

        },
        endDate(wellName) {
            let start_date = this.startDates[wellName];

            if (start_date === undefined)
                return undefined;

            let date = new Date(start_date);
            date.setDate(date.getDate() + this.modelInfo.outputChunkLength)
            return this.dateAsString(date)
        },
        dateAsString(date) {
            if (typeof (date) === 'string') {
                date = new Date(date);
                return date.toISOString().split('T')[0];
            } else {
                return date.toISOString().split('T')[0];
            }
        }
    },
    computed: {
        //dateBounds() {
        //    let results = { lower: undefined, upper: undefined }
        //    if (this.modelInfo === undefined || this.selectedWells.length === 0) {
        //        return results
        //    }

        //    let d = this.wellData;
        //    this.selectedWells.forEach(
        //        function (key) {
        //            let dateArray = d[key].date;

        //            if (dateArray.length != 0) {
        //                let l = new Date(dateArray[0]);
        //                let u = new Date(dateArray[dateArray.length - 1]);

        //                if (l < results.lower || results.lower === undefined) {
        //                    results.lower = l;
        //                }

        //                if (results.upper > u || results.upper === undefined) {
        //                    results.upper = u;
        //                }
        //            }
        //        }
        //    )
        //    console.log(results.lower.toISOString())

        //    results.lower.setDate(results.lower.getDate() - this.modelInfo.inputChunkLength)
        //    results.upper.setDate(results.upper.getDate() - this.modelInfo.outputChunkLength)

        //    let resultsAsStrings = {
        //        lower: this.dateAsString(results.lower),
        //        upper: this.dateAsString(results.upper)
        //    }

        //    console.log(resultsAsStrings);
        //    return resultsAsStrings;
        //},
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
    <div class="flex">
        <div class="col-1">
            <select multiple v-model="selectedWells" size="30">
                <option v-for="well in wells" :key="well">{{ well }}</option>
            </select>
        </div>

        <div class="col-2">
            <div v-for="sel in selectedWells" :key="sel">
                <div>
                    <label>
                        Prediction start:
                        <input type="date" v-model="startDates[sel]" />
                    </label>
                    <p v-if="endDate(sel) != undefined">End date (YYYY-MM-DD): {{ endDate(sel) }}</p>
                </div>
                <Plot :plot="createPlotlyLayout(sel)" />
            </div>
        </div>

        <div class="col-3">
            <button @click="predictSelection()">Predict</button>
        </div>
    </div>
</template>
