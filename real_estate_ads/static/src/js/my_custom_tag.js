odoo.define('real_estate_ads.CustomAction', function(require) {
    "use strict";

   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');

   var CustomAction = AbstractAction.extend({
        template: "CustomActions",
        start: function() {
            console.log("Action")
        }
   })

   core.action_registry.add("custom_client_action", CustomAction)

});