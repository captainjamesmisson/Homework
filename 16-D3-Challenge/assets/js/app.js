var svgWidth = 750
var svgHeight = 500

var margin = {
    top: 40,
    right: 40,
    bottom:70,
    left: 100 
};

var width = svgWidth-margin.left-margin.right;
var height = svgHeight-margin.top-margin.bottom;

var svg = d3.select("body").append("svg").attr("width",svgWidth).attr("height",svgHeight);

var chartGroup = svg.append("g").attr("transform",`translate(${margin.left}, ${margin.top})`);

d3.csv("assets/data/data.csv").then(function(censusData) {
    
    censusData.forEach(function(data) {
        data.poverty = +data.poverty;
        data.healthcare = +data.healthcare;
        data.abbr = data.abbr;
    });
    
    var xLinearScale = d3.scaleLinear().domain([8,d3.max(censusData,d=>d.poverty+2)]).range([0,width]);
    var yLinearScale = d3.scaleLinear().domain([2,d3.max(censusData, d=>d.healthcare+2)]).range([height,0]);

    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    chartGroup.append("g").attr("transform",`translate(0,${height})`).call(bottomAxis);
    chartGroup.append("g").call(leftAxis);
    
    var circlesGroup = chartGroup.selectAll("circle")
    .data(censusData)
    .enter()

    circlesGroup
    .append("circle")
    .attr("cx",d=>xLinearScale(d.poverty))
    .attr("cy",d=>yLinearScale(d.healthcare))
    .attr("r","10")
    .classed("stateCircle",true)
    .attr("opacity","0.8");

    
    textGroup = circlesGroup.append("text")
    .text(d=>d.abbr)
    .attr("dx",d=>xLinearScale(d.poverty))
    .attr("dy",d=>yLinearScale(d.healthcare))
    .classed("stateText",true);

    var toolTip = d3.tip().attr("class","d3-tip").offset([10,-20]).html(function(d){
        return(`% Lacking Health ${d.healthcare}<br>% in Poverty ${d.poverty}`)
    });

    chartGroup.call(toolTip);

    textGroup.on("mouseover",function(d){
        toolTip.show(d,this)})
        .on("mouseout",function(d){
            toolTip.hide(d)});

    // y-axis label
    chartGroup.append("text").attr("transform", "rotate(-90)").attr("y",0-margin.left+40).attr("x",0-(height/2))
    .attr("dy","1em").classed("aText",true).text("Lacks Healthcare (%)");

    // x-axis label
    chartGroup.append("text").attr("transform",`translate(${width/2},${height+margin.top+10})`)
    .classed("aText",true).text("Proverty Rate (%)");

})