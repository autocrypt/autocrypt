Tests = function() {
    var suites = {};
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

    function run() {
        var arr = Object.entries(suites)
        log('Running ' + arr.length + ' suites...');
        arr.forEach(runSuite);
        log(assertions + ' assertions. ' + failures + ' failures.');
    };

    function runSuite(suite) {
        var name = suite[0];
        var desc = suite[1];
        var specs = {};
        var it = function(behaves, fun) { specs[behaves] = fun };
        var env = {};
        desc.bind(env)(it, assert);
        Object.entries(specs).forEach(function (spec) {
            var name = spec[0];
            var task = spec[1];
            log('  ' + name);
            if (env.setup) env.setup();
            task();
            if (env.teardown) env.teardown();
        });
    };

    function describe(context, fun) {
        suites[context] = fun
    };

    return {
        describe: describe,
        run: run
    };
}();

