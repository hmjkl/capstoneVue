<script>
import Plotly from 'plotly.js-dist'

export default {
    props: {
        plot: Object
    },
    mounted() {
        Plotly.newPlot(this.$refs.plotdiv, this.plot.traces, this.plot.layout)
    }

}
</script>

<template>
    <div class="plot" ref="plotdiv">
    </div>
</template>
