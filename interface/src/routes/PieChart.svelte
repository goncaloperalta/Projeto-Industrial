<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    export let totalPresses = 0;     // Prop from page.svelte
    export let successfulPresses = 0; // Prop from page.svelte

    $: console.log("Total presses:", totalPresses, "Successful presses:", successfulPresses);

    let svgPie;

    // Reactive `dataPie` based on `totalPresses` and `successfulPresses`
    $: dataPie = [
    { label: "Success", value: successfulPresses || 0 },
    { label: "Failure", value: (totalPresses || 0) - (successfulPresses || 0) }
];

function drawPieChart() {
    console.log("Drawing pie chart with data:", dataPie);

    const width = 300;
    const height = 300;
    const radius = Math.min(width, height) / 2;

    const pie = d3.pie().value(d => d.value)(dataPie);
    const arc = d3.arc().outerRadius(radius).innerRadius(0);

    // Clear existing chart elements
    d3.select(svgPie).selectAll("*").remove();

    const color = d3.scaleOrdinal()
        .domain(["Success", "Failure"])
        .range(["#34D399", "#EF4444"]);

    const g = d3.select(svgPie).append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    g.selectAll("path")
        .data(pie)
        .join("path")
        .attr("d", arc)
        .attr("fill", d => color(d.data.label))
        .attr("stroke", "#fff")
        .style("stroke-width", "2px");

    g.selectAll("text")
        .data(pie)
        .join("text")
        .attr("transform", d => `translate(${arc.centroid(d)})`)
        .attr("text-anchor", "middle")
        .style("fill", "#fff")
        .style("font-weight", "bold")
        .text(d => `${d.data.label}: ${((d.data.value / totalPresses) * 100).toFixed(1)}%`);
}
    // Call `drawPieChart` whenever `dataPie` changes
    $: if (totalPresses && successfulPresses) drawPieChart();
</script>

<style>
    svg {
        width: 100%;
        height: 100%;
    }
</style>

<svg bind:this={svgPie} width={300} height={300}>
    <g transform="translate(150, 150)">
        <!-- Pie chart slices and labels will be appended here -->
    </g>
</svg>