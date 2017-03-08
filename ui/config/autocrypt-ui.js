// javascript implementation of essential Autocrypt preferences UI


ui = {};

panes = {};

user = 'User';

msgstore = {};

setup_page = function() {
    panes = {
        'compose': document.getElementById("compose"),
        'list': document.getElementById("list"),
        'msg-view': document.getElementById("msg-view"),
        'preferences': document.getElementById("preferences")
    };
    ui = {
        'more': document.getElementById("more"),
        'list-description': document.getElementById("list-description"),
        'menu-username': document.getElementById("menu-username"),
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
        'showmore': document.getElementById("showmore"),
        'reply': document.getElementById("reply"),
        'yes': document.getElementById("preferyes"),
        'no': document.getElementById("preferno"),
        'enable': document.getElementById("enable"),
        'description': document.getElementById("description"),
        'settings': document.getElementById("autocrypt-settings")
    };
    adduser('Alice');
    adduser('Bob');

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
    ac = msgstore[username]['autocrypt'];
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
    msgstore[user]['autocrypt']['enabled'] = ui['enable'].checked;
    update_description();
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
    ui['menu-username'].innerText = "Logged in as " + name;
    ui['from'].innerText = name;
    ui['list-description'].innerText = ""; // "Mailbox for " + name;
    setupprefs(name);
    ui['showmore'].checked = false;
    pane('list');
    update_description();
};

lockimg = function() {
    var lock = document.createElement('img');
    lock.src = 'file:///usr/share/icons/Tango/scalable/emblems/emblem-readonly.svg';
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
    } else if (choice == 'list') {
        populate_list();
        clearcompose();
    }
};

adduser = function(username) {
    if (msgstore[username] == undefined) {
        msgstore[username] = {
            'autocrypt': {
                'enabled': false
            },
            'msgs': []
        };
    }
};

autocryptheader = function(username) {
    if (msgstore[username] == undefined)
        return undefined;
    ac = msgstore[username]['autocrypt'];
    if (ac['enabled'] == false)
        return undefined;
    return { 'key': ac['key'],
             'prefer-encrypt': ac['prefer-encrypt']
           };
};

clearcompose = function() {
    ui['to'].value = '';
    ui['body'].value = '';
    ui['subject'].value = '';
    ui['encrypted'].checked = false;
};

show_msg = function(msg) {
    ui['view-from'].innerText = msg['from'];
    ui['view-to'].innerText = msg['to'];
    ui['view-subject'].innerText = msg['subject'];
    ui['view-date'].innerText = msg['date'];
    if (msg['encrypted'] == true) {
        ui['view-encrypted'].innerText = 'Message was encrypted';
    } else {
        ui['view-encrypted'].innerText = 'Message was not encrypted';
    }
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
    pane('compose');
};

generate_list_entry_from_msg = function(msg) {
    var ret = document.createElement('tr');
    ret.classList.add("message");
    ret.onclick = function() { show_msg(msg); };

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

    var e = document.createElement('td');
    if (msg['encrypted'])
        e.appendChild(lockimg());
    ret.appendChild(e);

    return ret;
};

populate_list = function() {
    msgs = msgstore[user]['msgs'];

    while (ui['msglist'].hasChildNodes())
        ui['msglist'].removeChild(ui['msglist'].lastChild);

    for (x in msgs) {
        ui['msglist'].appendChild(generate_list_entry_from_msg(msgs[x]));
    }
};

sendmail = function() {
    if (addmail(user, ui['to'].value, ui['subject'].value, ui['body'].value, ui['encrypted'].checked)) {
        clearcompose();
        pane('list');
        return false;
    } else {
        return false;
    }
};

addmail = function(from, to, subj, body, encrypted) {
    if (msgstore[from] == undefined) {
        alert("Not a valid sender: " + to);
        return false;
    }
    if (msgstore[to] == undefined) {
        alert("No recipient " + to);
        return false;
    }
    msg = { 'from': from,
            'to': to,
            'subject': subj,
            'body': body,
            'encrypted': encrypted,
            'autocrypt': autocryptheader(from),
            'date': Date()
          };
    msgstore[to].msgs.push(msg);
    msgstore[from].msgs.push(msg);
    return true;
};
