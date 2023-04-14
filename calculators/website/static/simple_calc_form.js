window.addEventListener('load', function() {
  var extinction_given_pre_equilibrium = document.getElementById('extinction_given_pre_equilibrium');
  var preindustrial_given_pre_equilibrium = document.getElementById('preindustrial_given_pre_equilibrium');

  var extinction_given_preindustrial = document.getElementById('extinction_given_preindustrial');
  var industrial_given_preindustrial = document.getElementById('industrial_given_preindustrial');

  var extinction_given_industrial = document.getElementById('extinction_given_industrial');
  var future_perils_given_industrial = document.getElementById('future_perils_given_industrial');

  var extinction_given_present_perils = document.getElementById('extinction_given_present_perils');
  var pre_equilibrium_given_present_perils = document.getElementById('pre_equilibrium_given_present_perils');
  var preindustrial_given_present_perils = document.getElementById('preindustrial_given_present_perils');
  var industrial_given_present_perils = document.getElementById('industrial_given_present_perils');
  var future_perils_given_present_perils = document.getElementById('future_perils_given_present_perils');
  var interstellar_given_present_perils = document.getElementById('interstellar_given_present_perils');
  var multiplanetary_given_present_perils = document.getElementById('multiplanetary_given_present_perils');

  var extinction_given_future_perils = document.getElementById('extinction_given_future_perils');
  var pre_equilibrium_given_future_perils = document.getElementById('pre_equilibrium_given_future_perils');
  var preindustrial_given_future_perils = document.getElementById('preindustrial_given_future_perils');
  var industrial_given_future_perils = document.getElementById('industrial_given_future_perils');
  var interstellar_given_future_perils = document.getElementById('interstellar_given_future_perils');
  var multiplanetary_given_future_perils = document.getElementById('multiplanetary_given_future_perils');

  var extinction_given_multiplanetary = document.getElementById('extinction_given_multiplanetary');
  var pre_equilibrium_given_multiplanetary = document.getElementById('pre_equilibrium_given_multiplanetary');
  var preindustrial_given_multiplanetary = document.getElementById('preindustrial_given_multiplanetary');
  var industrial_given_multiplanetary = document.getElementById('industrial_given_multiplanetary');
  var future_perils_given_multiplanetary = document.getElementById('future_perils_given_multiplanetary');
  var interstellar_given_multiplanetary = document.getElementById('interstellar_given_multiplanetary');


  // preindustrial_given_pre_equilibrium.value = 1 - extinction_given_pre_equilibrium.value;

  // extinction_given_pre_equilibrium.addEventListener('input', function() {
  //   preindustrial_given_pre_equilibrium.value = 1 - extinction_given_pre_equilibrium.value;
  // });


  function update_fields(target, sources) {
    var target = document.getElementById(target)
    var input_fields = sources.map(source => document.getElementById(source))
    function sum_input_fields(input_fields) {
      return input_fields.map(field => parseFloat(field.value)).reduce((partialSum, a) => partialSum + a, 0);
    };
    target.value = 1 - sum_input_fields(input_fields);

    input_fields.forEach((field) => {
      field.addEventListener('input', function() {
        target.value = 1 - sum_input_fields(input_fields)
      });
    });
  }

  update_fields('preindustrial_given_pre_equilibrium', ['extinction_given_pre_equilibrium'])
  update_fields('industrial_given_preindustrial', ['extinction_given_preindustrial'])
  update_fields('future_perils_given_industrial', ['extinction_given_industrial'])
  update_fields('multiplanetary_given_present_perils', ['extinction_given_present_perils',
    'pre_equilibrium_given_present_perils', 'preindustrial_given_present_perils',
    'industrial_given_present_perils', 'future_perils_given_present_perils',
    'interstellar_given_present_perils'])
  update_fields('multiplanetary_given_future_perils', ['extinction_given_future_perils',
    'pre_equilibrium_given_future_perils', 'preindustrial_given_future_perils',
    'industrial_given_future_perils', 'interstellar_given_future_perils'])
  update_fields('interstellar_given_multiplanetary', ['extinction_given_multiplanetary',
    'pre_equilibrium_given_multiplanetary', 'preindustrial_given_multiplanetary',
    'industrial_given_multiplanetary', 'future_perils_given_multiplanetary'])
});
