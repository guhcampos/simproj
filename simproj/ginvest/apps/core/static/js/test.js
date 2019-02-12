function prepend_warning() {
    $("body").prepend('<div id="development-warning">DEVELOPMENT FUNCTIONS ARE ENABLED</div>');
}

function post_data_to_simulation(data_to_post) {
  // Enviamos dados para o backend via AJAX
  $.ajax({
    type: "POST",
    url:"/fluxo/post/",
    data: { "req": JSON.stringify(data_to_post)},
    dataType: "json",
    success: workProcessedData,
  });
}

function test_fixed_income() {

  prepend_warning();

  console.log("DEBUG ENABLED: test_fixedincome");
  $("#select-titulo").val(1);
  $("#input-valorinvestido").val("1000,00");
  $("#input-taxadecustodia").val("0.4%");

  $("#submit").click();
}

function test_simulation() {

  prepend_warning();

  console.log("DEBUG ENABLED: test_simulation");
  mdata = [];

  mdata[0] = ['P','2014-06-25','-14337.00'];
  mdata[1] = ['Q','2014-07-26','18997.00'];
  mdata[2] = ['R','2014-08-27',"2438.00"];
  mdata[3] = ['S','2014-09-28','-633.17'];
  mdata[4] = ['T','2014-10-29','-20.00'];
  mdata[5] = ['U','2014-11-30','-45.00'];
  mdata[6] = ['V','2014-12-01','200.00'];
  mdata[7] = ['W','2015-01-02','999.00'];
  mdata[8] = ['X','2015-02-03','666.00'];
  mdata[9] = ['Y','2015-03-04','-666.00'];
  mdata[10] = ['Z','2015-04-05','317.00'];

  var req = {};
  req.dados = mdata;
  req.conf = {};
  req.conf.selic = $("#config-selic").is(":checked");
  req.conf.ipca = $("#config-inflacao-ipca").is(":checked");
  req.conf.igpm = $("#config-inflacao-igpm").is(":checked");

  post_data_to_simulation(req);
}