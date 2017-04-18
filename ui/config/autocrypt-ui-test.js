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
    assert.content = function(text, id) {
        elem = document.getElementById(id);
        assert( elem.innerText == text,
                id + ' should contain "' + text + '".' );
    };
    function it(behaves, fun) {
        log('  ' + behaves);
        it.setup();
        fun();
        it.teardown();
    };
    function run() {
        var arr = Object.entries(tests)
        log('Running ' + arr.length + ' tests...');
        arr.forEach(function(elem) {
            it.setup = function() {};
            it.teardown = function() {};
            log(elem[0] + '...');
            elem[1](it, assert);
        });
        log(assertions + ' assertions. ' + failures + ' failures.');
    };
    return {
        describe: function(context, fun) { tests[context] = fun },
        run: run
    };
}();

Tests.describe('User switch', function(it, assert) {
    var usertoggle = document.getElementById("usertoggle");
    it.teardown = function() {
        switchuser('alice');
    };
    it('starts with Alice', function() {
        assert.content('Alice', 'username');
    });
    it('switches to Bob', function() {
        usertoggle.click();
        assert.content('Bob', 'username');
    });
    it('switches back to Alice', function() {
        usertoggle.click();
        usertoggle.click();
        assert.content('Alice', 'username');
    });
});

