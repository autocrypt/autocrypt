(function(){
    var describe = Tests.describe;
    describe('User switch', function(it, assert) {
        var usertoggle = document.getElementById("usertoggle");
        this.teardown = function() {
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
})();
