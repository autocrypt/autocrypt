// javascript implementation of essential Autocrypt preferences UI


ui = {};

panes = {};

user = 'User';

msgstore = {};

replying_to = undefined;

setup_page = function() {
    panes = {
        'compose': document.getElementById("compose"),
        'list': document.getElementById("list"),
        'msg-view': document.getElementById("msg-view"),
        'preferences': document.getElementById("preferences")
    };
    ui = {
        'more': document.getElementById("more"),
        'list-replacement': document.getElementById("list-replacement"),
        'msgtable': document.getElementById("msgtable"),
        'username': document.getElementById("username"),
        'from': document.getElementById("from"),
        'to': document.getElementById("to"),
        'subject': document.getElementById("subject"),
        'body': document.getElementById("body"),
        'msglist': document.getElementById("msglist"),
        'view-from': document.getElementById("view-from"),
        'view-to': document.getElementById("view-to"),
        'view-subject': document.getElementById("view-subject"),
        'view-date': document.getElementById("view-date"),
        'view-body': document.getElementById("view-body"),
        'view-encrypted': document.getElementById("view-encrypted"),
        'encrypted': document.getElementById("encrypted"),
        'encrypted-row': document.getElementById("encrypted-row"),
        'showmore': document.getElementById("showmore"),
        'reply': document.getElementById("reply"),
        'yes': document.getElementById("preferyes"),
        'no': document.getElementById("preferno"),
        'enable': document.getElementById("enable"),
        'description': document.getElementById("description"),
        'explanation': document.getElementById("explanation"),
        'settings': document.getElementById("autocrypt-settings")
    };
    adduser('Alice', 'green');
    adduser('Bob', 'darkorange');
    ui['encrypted'].parentNode.insertBefore(img('lock'), ui['encrypted']);

    switchuser(Object.keys(msgstore)[0]);
    pane('list');
    update_description();
};

autocrypt_preference = function(p) {
    if (p == 'yes') {
        other = 'no';
    } else {
        other = 'yes';
        p = 'no';
    };

    ui[other].checked = false;
    if (ui['yes'].checked) {
        msgstore[user]['autocrypt']['prefer-encrypted'] = true;
    } else if (ui['no'].checked) {
        msgstore[user]['autocrypt']['prefer-encrypted'] = false;
    } else {
        delete msgstore[user]['autocrypt']['prefer-encrypted'];
    }
    self_sync_autocrypt_state(user);
    update_description();
};

get_description = function() {
    if (!ui['enable'].checked) {
        return 'Autocrypt is disabled on this device.';
    }
    if (ui['yes'].checked) {
        return 'Autocrypt will encourage your peers to send you encrypted mail.';
    }
    if (ui['no'].checked) {
        return 'Autocrypt will discourage your peers from sending you encrypted mail.';
    }
    return 'Autocrypt lets your peers choose whether to send you encrypted mail.';
};

more = function() {
    ui['showmore'].checked = !ui['showmore'].checked;
    update_description();
    return false;
};

setupprefs = function(username) {
    ac = msgstore[username.toLowerCase()]['autocrypt'];
    ui['enable'].checked = ac['enabled'];
    if (ac['prefer-encrypted'] == undefined) {
        ui['yes'].checked = false;
        ui['no'].checked = false;
    } else if (ac['prefer-encrypted'] == true) {
        ui['yes'].checked = true;
        ui['no'].checked = false;
    } else if (ac['prefer-encrypted'] == false) {
        ui['yes'].checked = false;
        ui['no'].checked = true;
    }
};

autocrypt_enable = function() {
    autocrypt_switch(user, ui['enable'].checked);
    update_description();
};

autocrypt_switch = function(username, enabled) {
    msgstore[username]['autocrypt']['enabled'] = enabled;
    if (enabled) {
        if (msgstore[username]['autocrypt']['key'] === undefined)
            msgstore[username]['autocrypt']['key'] = String(Math.random());
    }
    self_sync_autocrypt_state(username);
};

self_sync_autocrypt_state = function(username) {
    if (msgstore[username]['autocrypt']['enabled']) {
        msgstore[username]['autocrypt']['state'][username] = {
            'date': new Date(),
            'key': msgstore[username]['autocrypt']['key'],
            'prefer-encrypted': msgstore[username]['autocrypt']['prefer-encrypted']
        };
    } else {
        msgstore[username]['autocrypt']['state'][username] = {
            'date': new Date()
        };
    }
};

enablecheckbox = function(box, enabled) {
    box.disabled = !enabled;
    if (enabled)
        box.parentElement.classList.remove('disabled');
    else
        box.parentElement.classList.add('disabled');
};

update_description = function() {
    disabled = !ui['enable'].checked;
    ui['yes'].disabled = disabled;
    ui['no'].disabled = disabled;
    if (ui['showmore'].checked) {
        ui['settings'].style.display = 'block';
        ui['showmore'].innerText = 'Hide Advanced Settings';
    } else {
        ui['settings'].style.display = 'none';
        ui['showmore'].innerText = 'Advanced Settings...';
    }
    if (disabled) {
        ui['yes'].parentElement.classList.add('disabled');
        ui['no'].parentElement.classList.add('disabled');
        ui['more'].style.display = 'none';
    } else {
        ui['yes'].parentElement.classList.remove('disabled');
        ui['no'].parentElement.classList.remove('disabled');
        ui['more'].style.display = 'block';
    };
    ui['description'].innerText = get_description();
};

changeuser = function() {
    names = Object.keys(msgstore);
    index = -1;
    for (var x in names) {
        if (names[x] == user) {
            index = x;
        }
    }
    newindex = (Number(index) + 1) % (names.length);
    switchuser(names[newindex]);
    return false;
};

switchuser = function(name) {
    user = name;
    ui['username'].innerText = msgstore[name]['name'];
    ui['username'].style.color = msgstore[name]['color'];
    ui['from'].innerText = msgstore[name]['name'];
    setupprefs(name);
    ui['showmore'].checked = false;
    pane('list');
    update_description();
};

img = function(what) {
    var index = {
        'lock': 'file:///usr/share/icons/Tango/16x16/emblems/emblem-readonly.png',
        'back': 'file:///usr/share/icons/Tango/16x16/actions/back.png',
        'forward': 'file:///usr/share/icons/Tango/16x16/actions/forward.png'
    };
    var lock = document.createElement('img');
    lock.src = index[what];
    return lock;
};

pane = function(choice) {
    for (var x in panes) {
        panes[x].style.display = 'none';
        e = document.getElementById("tab-" + x);
        if (e) {
            e.classList.remove('selected');
        }
    }
    panes[choice].style.display = 'block';
    n = "tab-" + choice;
    e = document.getElementById(n);
    if (e) {
        e.classList.add('selected');
    }
    if (choice == 'compose') {
        ui['to'].focus();
        updatecompose();
    } else if (choice == 'list') {
        populate_list();
        clearcompose();
    }
};

adduser = function(username, color) {
    lc = username.toLowerCase();
    if (msgstore[lc] == undefined) {
        msgstore[lc] = {
            'name': username,
            'color': color,
            'autocrypt': {
                'enabled': false,
                'state': {}
            },
            'msgs': []
        };
    }
};

autocryptheader = function(username) {
    var lc = username.toLowerCase();
    if (msgstore[lc] == undefined)
        return undefined;
    ac = msgstore[lc]['autocrypt'];
    if (ac['enabled'] == false)
        return undefined;
    return { 'key': ac['key'],
             'prefer-encrypted': ac['prefer-encrypted']
           };
};

clearcompose = function() {
    ui['to'].value = '';
    ui['body'].value = '';
    ui['subject'].value = '';
    ui['encrypted'].checked = false;
};

get_encryption_status_node = function(encrypted) {
    var x = document.createElement('span');
    if (encrypted) {
        var sub = document.createElement('span');
        x.appendChild(img('lock'));
        sub.innerText = "Message was encrypted";
        x.appendChild(sub);
    } else {
        x.innerText = "Message was not encrypted";
    }

    return x;
};

show_msg = function(msg) {
    ui['view-from'].innerText = msg['from'];
    ui['view-to'].innerText = msg['to'];
    ui['view-subject'].innerText = msg['subject'];
    ui['view-date'].innerText = msg['date'];
    ui['view-encrypted'].replaceChild(get_encryption_status_node(msg['encrypted']), ui['view-encrypted'].childNodes[0]);
    ui['view-body'].innerText = msg['body'];

    if (msg['from'] == user) {
        ui['reply'].style.display = 'none';
    } else {
        ui['reply'].style.display = 'inline';
        ui['reply'].onclick = function() { reply_to_msg(msg); };
    }

    pane('msg-view');
};

indent = function(str) {
    return str.split('\n').map(function(y) { return "> " + y; }).join('\n');
};

reply_to_msg = function(msg) {
    ui['to'].value = msg['from'];
    ui['subject'].value = 'Re: ' + msg['subject'];
    ui['body'].value = indent(msg['body']);
    replying_to = msg;
    pane('compose');
};

generate_list_entry_from_msg = function(msg) {
    var ret = document.createElement('tr');
    ret.classList.add("message");
    ret.onclick = function() { show_msg(msg); };

    var e = document.createElement('td');
    if (msg['encrypted'])
        e.appendChild(img('lock'));
    if (msg['to'].toLowerCase() == user)
        e.appendChild(img('back'));
    if (msg['from'].toLowerCase() == user)
        e.appendChild(img('forward'));
    ret.appendChild(e);

    var f = document.createElement('td');
    f.innerText = msg['from'];
    ret.appendChild(f);

    var t = document.createElement('td');
    t.innerText = msg['to'];
    ret.appendChild(t);

    var s = document.createElement('td');
    s.innerText = msg['subject'];
    ret.appendChild(s);

    var d = document.createElement('td');
    d.innerText = msg['date'];
    ret.appendChild(d);

    return ret;
};

populate_list = function() {
    var msgs = msgstore[user]['msgs'];

    while (ui['msglist'].hasChildNodes())
        ui['msglist'].removeChild(ui['msglist'].lastChild);

    if (msgs.length) {
        for (var x in msgs) {
            ui['msglist'].appendChild(generate_list_entry_from_msg(msgs[x]));
        }
        ui['list-replacement'].style.display = 'none';
        ui['msgtable'].style.display = 'table';
    } else {
        ui['list-replacement'].style.display = 'block';
        ui['msgtable'].style.display = 'none';
    }
};

sendmail = function() {
    if (addmail(msgstore[user]['name'], ui['to'].value, ui['subject'].value, ui['body'].value, ui['encrypted'].checked)) {
        clearcompose();
        pane('list');
        return false;
    } else {
        return false;
    }
};

addmail = function(from, to, subj, body, encrypted) {
    if (msgstore[from.toLowerCase()] == undefined) {
        alert("Not a valid sender: " + to);
        return false;
    }
    if (msgstore[to.toLowerCase()] == undefined) {
        alert("No recipient " + to);
        return false;
    }
    var msg = { 'from': from,
            'to': to,
            'subject': subj,
            'body': body,
            'encrypted': encrypted,
            'autocrypt': autocryptheader(from),
            'date': new Date()
              };
    storemail(to, msg);
    if (to.toLowerCase() != from.toLowerCase())
        storemail(from, msg);
    return true;
};

getacforpeer = function(username, peer) {
    var ac = msgstore[username.toLowerCase()]['autocrypt']['state'][peer.toLowerCase()];

    if (ac === undefined)
        ac = { 'date': new Date("1970") };
    return ac;
};

acupdate = function(username, msg) {
    var ac = getacforpeer(username, msg['from']);
    var newac = {
        'date': msg['date']
    };
    if (msg['autocrypt'] === undefined) {
    } else {
        newac['prefer-encrypted'] = msg['autocrypt']['prefer-encrypted'];
        newac['key'] =  msg['autocrypt']['key'];
    };
    if (ac['date'].getTime() < newac['date'].getTime()) {
        msgstore[username]['autocrypt']['state'][msg['from'].toLowerCase()] = newac;
    }
};

storemail = function(username, msg) {
    var lc = username.toLowerCase();
    acupdate(lc, msg);
    msgstore[lc]['msgs'].push(msg);
};

updatecompose = function() {
    var to = ui['to'].value;
    var ac = getacforpeer(user,to);

    if (!msgstore[user]['autocrypt']['enabled']) {
        if (ac['prefer-encrypted']) {
            ui['encrypted-row'].style.display = 'table-row';
            ui['encrypted'].checked = false;
            enablecheckbox(ui['encrypted'], true);
            ui['explanation'].innerText = 'enable Autocrypt to encrypt';
        } else {
            ui['encrypted-row'].style.display = 'none';
        }
    } else {
        ui['encrypted-row'].style.display = 'table-row';
        if (ac['key'] !== undefined) {
            ui['encrypted'].checked = ac['prefer-encrypted'];
            enablecheckbox(ui['encrypted'], true);
            ui['explanation'].innerText = '';
        } else {
            ui['encrypted'].checked = false;
            enablecheckbox(ui['encrypted'], false);
            if (to == '')
                ui['explanation'].innerText = 'please choose a recipient';
            else
                ui['explanation'].innerText = 'If you want to encrypt to ' + to + ', ask ' + to + ' to enable Autocrypt and send you an e-mail';
        }
    }
};

clickencrypted = function() {
    var to = ui['to'].value;
    var ac = getacforpeer(user, to);
    var encrypted = ui['encrypted'].checked;

    // FIXME: if autocrypt is disabled and we've set encrypt, prompt the user about it.
    if (encrypted && msgstore[user]['autocrypt']['enabled'] === false) {
        if (confirm("Please only enable Autocrypt on one device.\n\n" +
                    "Are you sure you want to enable Autocrypt on this device?")) {
            autocrypt_switch(user, true);
            setupprefs(user);
            update_description();
        } else {
            ui['encrypted'].checked = false;
            encrypted = false;
        }
    }
    if (!msgstore[user]['autocrypt']['enabled'] && !ui['encrypted'].disabled) {
        ui['explanation'].innerText = 'enable Autocrypt to encrypt';
    } else if (encrypted && ac['prefer-encrypted'] === false) {
        ui['explanation'].innerText = to + ' prefers to receive unencrypted mail.  It might be hard for them to read.';
    } else if (!encrypted && ac['prefer-encrypted'] === true) {
        ui['explanation'].innerText = to + ' prefers to receive encrypted mail!';
    }  else {
        ui['explanation'].innerText = '';
    }
};
