Tests = function() {
    var env = {specs: {}};
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
        var arr = Object.entries(this.specs)
        log('Running ' + arr.length + ' suites...');
        arr.forEach(function (suite) {
            var name = suite[0];
            var desc = suite[1];
            var env = {specs: {}};
            log('  ' + name);
            desc.bind(env)(describe.bind(env), assert);
            runSuite.bind(env)();
        });
        log(assertions + ' assertions. ' + failures + ' failures.');
    };

    function runSuite() {
        var arr = Object.entries(this.specs)
        var setup = this.setup;
        var teardown = this.teardown;
        log('  Running ' + arr.length + ' specs...');
        arr.forEach(function (spec) {
            var name = spec[0];
            var task = spec[1];
            log('     ' + name);
            if (setup) setup();
            task();
            if (teardown) teardown();
        });
    };

    function describe(context, fun) {
        this.specs[context] = fun
    };

    return {
        describe: describe.bind(env),
        run: run.bind(env)
    };
}();

