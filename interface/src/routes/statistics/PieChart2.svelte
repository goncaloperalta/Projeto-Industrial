<script>
    import * as d3 from 'd3'
    import { onMount } from 'svelte';

    let {successRate} = $props();
    let data = [successRate, 100 - successRate];
    let element;
    
    onMount(() => {
        let width = 350, height = 350, radius = Math.min(width, height)/2;
        
        var svg = d3.select(element)
            .attr("width", width)
            .attr("height", height);

        var g = svg.append("g")
            .attr("transform", "translate(" + radius + "," + radius + ")");

        var color = d3.scaleOrdinal(["#aac597","#ef6d80"]);

        var pie = d3.pie().value((d) => {
            return d;
        })
        
        var path = d3.arc()
            .outerRadius(radius)
            .innerRadius(100);

        var arc = g.selectAll("arc")
            .data(pie(data))
            .enter()
            .append("g");

        arc.append("path")
            .attr("d", path)
            .attr("fill", (d) => {
                return color(d.data);
            });

        var label = d3.arc()
            .outerRadius(radius)
            .innerRadius(100);

        arc.append("text")
            .attr("transform", (d) => {
                return "translate(" + label.centroid(d) + ")";
            })
            .attr("text-anchor", "middle")
            .text((d) => {
                return d.data.toFixed(1) + "%";
            })
            .style("fill", "white");
    })
</script>

<svg bind:this={element}></svg>

<style></style>