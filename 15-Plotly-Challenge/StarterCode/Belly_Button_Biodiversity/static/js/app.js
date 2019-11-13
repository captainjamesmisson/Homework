function buildMetadata(sample) {
  // @TODO: Complete the following function that builds the metadata panel
  // Use `d3.json` to fetch the metadata for a sample
  var sample_metadata_url = "/metadata/" +sample;
  d3.json(sample_metadata_url).then(function(sample_metadata){
    // Use d3 to select the panel with id of `#sample-metadata`
    var panel = d3.select("#sample-metadata");  
    // Use `.html("") to clear any existing metadata
    panel.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(sample_metadata).forEach(([key,value])=>{
    panel.append("p").text(`${key}: ${value}`);
    });
    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
  });
}

function buildCharts(sample) {
  // @TODO: Use `d3.json` to fetch the sample data for the plots
  var sample_data_url = "/samples/" +sample;
  d3.json(sample_data_url).then(function(data){
    // @TODO: Build a Bubble Chart using the sample data
    var trace1 = {
      type: "scatter",
      mode: "markers",
      x:data.otu_ids,
      y:data.sample_values,
      text: data.otu_labels,  
      marker: {
        color: data.otu_ids,
        size: data.sample_values,
        colorscale: 'Earth'}
      };
    
    var layout = {
      height: 500,
      width: 1250,
    };
    var bubblechart = [trace1];
    // var bubbleid = d3.select("#bubble");
    Plotly.newPlot('bubble', bubblechart, layout);

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).

    var trace2 = {
      values:data.sample_values.slice(0,10),
      labels: data.otu_ids.slice(0,10),
      hovertext: data.otu_labels.slice(0,10),
      hoverinfo:'hovertext',
      type: 'pie'};

    var layout = {
      height: 500,
      width: 850
    };

    var piechart = [trace2];
    
    Plotly.newPlot("pie",piechart, layout)
    
    });
  }
function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
