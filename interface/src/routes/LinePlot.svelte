<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    // Data points
    let { X, Y } = $props()

    // Combine X and Y into a single array of objects for D3 to work with
    const data = X.map((x, i) => ({ x, y: Y[i] }));

    // Dimensions for the SVG container
    const width = 500;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 50, left: 50 };
    
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    let svg;

    onMount(() => {
        const xScale = d3.scaleLinear()
            .domain([d3.min(X), d3.max(X)])  // Set the domain of X axis based on the data
            .range([0, innerWidth]);

        const yScale = d3.scaleLinear()
            .domain([d3.min(Y), d3.max(Y)])  // Set the domain of Y axis based on the data
            .range([innerHeight, 0]);

        // Create line generator
        const line = d3.line()
            .x(d => xScale(d.x))
            .y(d => yScale(d.y));

        // Append the line to the SVG
        d3.select(svg)
            .select("g")
            .append("path")
            .data([data])
            .attr("class", "line")
            .attr("d", line)
            .attr("fill", "none")
            .attr("stroke", "#DA8359")
            .attr("stroke-width", 2);

        // Add X axis
        d3.select(svg)
            .select("g")
            .append("g")
            .attr("transform", `translate(0,${innerHeight})`)
            .call(d3.axisBottom(xScale));

        // Add Y axis
        d3.select(svg)
            .select("g")
            .append("g")
            .call(d3.axisLeft(yScale));

        // Add X-axis label
        d3.select(svg)
            .select("g")
            .append("text")
            .attr("class", "x-axis-label")
            .attr("x", innerWidth / 2) // Position it in the middle of the X axis
            .attr("y", innerHeight + margin.bottom - 10) // Move it below the X axis with padding
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("fill", "black") // Set label text color
            .text("Time (sec)");

        // Add Y-axis label
        d3.select(svg)
            .select("g")
            .append("text")
            .attr("class", "y-axis-label")
            .attr("x", -innerHeight / 2) // Position it in the middle of the Y axis
            .attr("y", -margin.left + 15) // Adjust the padding to keep it clear from the axis line
            .attr("transform", "rotate(-90)") // Rotate for vertical alignment
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("fill", "black") // Set label text color
            .text("Applied Force (N)");
    });
</script>

<style>
    svg {
        width: 100%;
        height: 100%;
    }
</style>

<svg bind:this={svg} width={width} height={height}>
    <g transform={`translate(${margin.left},${margin.top})`}>
        <!-- X and Y axes will be appended here by D3 -->
    </g>
</svg>