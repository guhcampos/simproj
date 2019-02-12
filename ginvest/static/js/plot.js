function plotNPV(npvplotdata) {

  // the actual data is an array inside the object
  var data = npvplotdata.cashflow;

  // the plot area
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 800 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

  // the plotting object
  var svg = d3.select("#graph-npv").attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom).append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Scales
  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([0, height]);

  // parses the data into understandable format
  data.forEach(function(d) {
    d.date = d3.time.format("%Y%m%d").parse(d.date);
  });

  // Axes
  var xAxis = d3.svg.axis().scale(x).orient("bottom").tickFormat(d3.time.format("%d/%m"));
  var yAxis = d3.svg.axis().scale(y).orient("left");

  // Sets the domain of x() to all possible values
  x.domain(d3.extent(data, function(d) { return d.date; }));

  // And the y() domain has been provided by code
  y.domain([npvplotdata.yrange, -npvplotdata.yrange]);

  // Create the gradient so the fill color of the bars changes with size
  svg.append("linearGradient")
      .attr("id", "balance-gradient")
      .attr("gradientUnits", "userSpaceOnUse")
      .attr("x1", 0).attr("y1", y(npvplotdata.yrange))
      .attr("x2", 0).attr("y2", y(-npvplotdata.yrange))
        .selectAll("stop")
          .data([
            {offset: "0%", color: "#44AA00"},
            {offset: "50%", color: "#CCFFAA"},
            {offset: "50%", color: "#FFAAAA" },
            {offset: "100%", color: "#D40000"}
          ])
          .enter().append("stop")
            .attr("offset", function(d) { return d.offset; })
            .attr("stop-color", function(d) { return d.color; });

  // Plot the bars
  svg.selectAll(".bar")
    .data(data)
    .enter()
    .append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.date);})
      .attr("y", function(d) { return y(Math.max(0, d.balance));})
      .attr("width", function(d) { return width / data.length; })
      .attr("height", function(d) { return Math.abs(y(d.balance)-y(0));});

  // Plot text labels
  // svg.selectAll(".barlabel")
  //   .data(data)
  //   .enter()
  //     .append("text")
  //     .attr("class", "barlabel")      
  //     .attr("x", function(d) { return x(d.date);})
  //     .attr("y", function(d) { return y(Math.min(0, d.balance))})
  //     .text(function(d){return d.balance})
  //     .attr("text-anchor", "middle")

  // Y Axis
  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Saldo (R$)");

  // X Axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height/2 + ")")
      .call(xAxis);

}