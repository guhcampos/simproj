/*
    Original Format:
    {
        "chart_data": 
        [
            {
            "name": "name of the series",
            "values": [ 
                [ valueofx, valueofy ],
                .
                .
                .
                ]
            }
        ]
        .
        .
        .
    }

    Derired Format:
    [
        {
            name: "name of the series",
            data: [
                { x: valueofx, y: valueofy },
                .
                .
                .
            ],
            color: palette.color()
        }
        .
        .
        .
    ]

*/
function convert_data(data) {

    var palette = new Rickshaw.Color.Palette();
    var converted = [];

    data.chart_data.forEach(function(serie){
        converted.push(
        {
            name: serie.name,
            color: palette.color(),
            data: $.map(serie.values, function(values){
                return {
                    x: parseInt(values[0], 10), y: parseFloat(values[1])
                };
            })
        }
        );
    });

    return converted;
}