// javascript implementation of essential Autocrypt preferences UI


get_ui = function() {
    return {
        'yes': document.getElementById("preferyes"),
        'no': document.getElementById("preferno"),
        'disable': document.getElementById("disable"),
        'description': document.getElementById("description")
    };
};

autocrypt_disable = function() {
    ui = get_ui();
    disabled = !ui['yes'].disabled;
    ui['yes'].disabled = disabled;
    ui['no'].disabled = disabled;
    if (disabled) {
        ui['yes'].parentElement.classList.add('disabled');
        ui['no'].parentElement.classList.add('disabled');
    } else {
        ui['yes'].parentElement.classList.remove('disabled');
        ui['no'].parentElement.classList.remove('disabled');
    };
    update_description();
};

autocrypt_preference = function(p) {
    ui = get_ui();

    if (p == 'yes') {
        other = 'no';
    } else {
        other = 'yes';
        p = 'no';
    };

    ui[other].checked = false;
    update_description();
};

get_description = function() {
    ui = get_ui();
    if (ui['disable'].checked) {
        return 'Autocrypt is disabled.  No e-mail headers will be sent.';
    }
    if (ui['yes'].checked) {
        return 'Autocrypt will encourage your peers to send you encrypted mail.';
    }
    if (ui['no'].checked) {
        return 'Autocrypt will discourage your peers from sending you encrypted mail.';
    }
    return 'Autocrypt lets your peers choose whether to send you encrypted mail.';
};

update_description = function() {
    ui = get_ui();
    ui['description'].innerText = get_description();
};
