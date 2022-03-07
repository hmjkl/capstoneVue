<script>
import Plotly from 'plotly.js-dist'

export default {
    props: {
        plot: Object
    },
    methods: {
        drawPlot() {
            Plotly.newPlot(this.$refs.plotdiv, this.plot.traces, this.plot.layout)
        }
    },
    mounted() {
        this.drawPlot()
    },
    watch: {
        plot() {
            this.drawPlot();
        }
    }

}
</script>

<template>
    <div class="plot" ref="plotdiv">
    </div>
</template>
