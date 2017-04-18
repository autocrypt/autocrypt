Tests = function() {
    var tests = {};
    var assertions = 0;
    var failures = 0;
    function log(message) {
        console.log( '%c ' + message, 'color: #444');
    }
    function fail(message) {
        console.log( '%c ' + message, 'color: red');
    }
    function assert(truth, message) {
        assertions = assertions + 1;
        if (!truth) {
            failures = failures + 1;
            fail("   " + message);
        }
    };
    function run() {
        var arr = Object.entries(tests)
        log('Running ' + arr.length + ' tests...');
        arr.forEach(function(elem) {
            log(elem[0] + '...');
            elem[1](assert);
        });
        log(assertions + ' assertions. ' + failures + ' failures.');
    };
    return {
        add: function(name, fun) { tests[name] = fun },
        run: run
    };
}();

Tests.add('Initial user', function(assert) {
    username = document.getElementById("username");
    assert(username.innerText == 'Alice', 'username should be Alice');
});

Tests.add('Switching users', function(assert) {
    usertoggle = document.getElementById("usertoggle");
    usertoggle.click();
    username = document.getElementById("username");
    assert(username.innerText == 'Bob', 'username should be Bob');
});
