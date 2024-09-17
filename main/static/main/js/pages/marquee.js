"use strict";

/**
 *   __  __                                      _  _____
 *  |  \/  |                                    | |/ ____|
 *  | \  / | __ _ _ __ __ _ _   _  ___  ___     | | (___
 *  | |\/| |/ _` | '__/ _` | | | |/ _ \/ _ \_   | |\___ \
 *  | |  | | (_| | | | (_| | |_| |  __/  __/ |__| |____) |
 *  |_|  |_|\__,_|_|  \__, |\__,_|\___|\___|\____/|_____/
 *                       | |
 *                       |_|
 *
 * MarqueeJS by Elias Ritter
 *
 * @version 1.0.0
 * @license GNU General Public License (GPL) 3.0 or later.
 * @author Elias Ritter
 */

function MarqueeJS(selector) {
    this._params = {
        duration: 50,
        direction: "rtl",
        pauseOnHover: false,
        iterations: 5,
        loop: true,
        timingFunction: "linear",
        hideOnPrint: true
    };

    this._selector = selector || ".marquee";
    this._keyframeId = this._generateUniqueId();
    this._stylenode = document.createElement("style");
}

MarqueeJS.prototype._generateUniqueId = function () {
    return Math.random().toString(36).substring(2);
};

MarqueeJS.prototype._log = function(msg, type) {
    type = type || "info";
    msg = "MarqueeJS: " + msg;
    if(typeof console[type] !== "function") {
        type = "log";
    }

    console[type](msg);
};

MarqueeJS.prototype.init = function (params) {
    params = params || {};
    const items = this._grabMarqueesFromDOM();

    if(items.length === 0) {
        return;
    }

    if (typeof params === 'object' && Object.getPrototypeOf(params) === Object.prototype) {
        this._parseParams(params);
    } else {
        this._log("Invalid parameter (params) given. Continuing with default parameters", 'warn')
    }

    this._generateKeyframeSet(this._params.direction);

    if(Boolean(this._params.hideOnPrint) === true) {
        this._bindCSSRule("@media print{" + this._selector + "{display:none!important;}}")
    }

    var initializedElements = 0;
    for (var i = 0; i < items.length; i++) {
        var marquee = items[i];
        if (this._applyAnimation(marquee)) initializedElements++;
    }

    this._log(String(initializedElements) + " Elements initialized");
    document.head.appendChild(this._stylenode);
    return this;
};

MarqueeJS.prototype._bindCSSRule = function(style) {
    this._stylenode.appendChild(document.createTextNode(style));
}

MarqueeJS.prototype._generateKeyframeSet = function (direction) {
    var from;
    var to;

    switch (direction.toLowerCase()) {
        case "ltr":
            from = -100;
            to = 0;
            break;

        case "rtl":
            from = 0;
            to = -50;
            break;
    }

    this._bindCSSRule(
        "@keyframes marqueejs"
        + this._keyframeId +
        "{0%{transform:translateX("
        + String(from) +
        "%);}100%{transform:translateX("
        + String(to) +
        "%);}}"
    );
};

MarqueeJS.prototype._parseParams = function (params) {
    this._params = Object.assign({}, this._params, params);
};

MarqueeJS.prototype._grabMarqueesFromDOM = function () {
    var marquees = [];
    var nodes = document.querySelectorAll(this._selector);

    outerLoop:
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];

            if (node.children.length !== 1) {
                continue;
            }

            for (var j = 0; j < node.children.length; j++) {
                var child = node.children[j];
                if (!child.classList.contains("marquee-content")) {
                    this._log("A Marquee is not well formed and was therefore skipped", "warn");
                    continue outerLoop;
                }
            }
            marquees.push(node);
        }
    return marquees;
};

MarqueeJS.prototype._appendStylesToNode = function(node, styles) {
    for(var property in styles) {
        if(property in node.style) {
            node.style[property] = styles[property];
        }
    }
};

MarqueeJS.prototype._applyAnimation = function (marquee) {
    var inner = marquee.children[0];
    var iterations;

    if (Boolean(this._params.pauseOnHover) === true) {
        marquee.addEventListener("mouseenter", function () {
            inner.style.animationPlayState = "paused";
        });

        marquee.addEventListener("mouseleave", function () {
            inner.style.animationPlayState = "running";
        });
    }

    if (Boolean(this._params.loop) === true || isNaN(this._params.iterations)) {
        iterations = "infinite";
    } else if (!isNaN(this._params.iterations)) {
        iterations = Math.abs(parseInt(this._params.iterations));
    }

    this._appendStylesToNode(marquee, {
        width: "100%",
        overflow: "hidden",
        whiteSpace: "nowrap",
        boxSizing: "border-box"
    });

    this._appendStylesToNode(inner, {
        willChange: "transform",
        display: "inline-block",
        // paddingLeft: "0",
        // width: "100%",
        animationName: "marqueejs" + this._keyframeId,
        animationDuration: String(Math.abs(this._params.duration)) + "s",
        animationTimingFunction: this._params.timingFunction,
        animationIterationCount: iterations,
        animationPlayState: "running"
    });

    return true;
};

document.addEventListener('DOMContentLoaded', function() {
    new MarqueeJS("#marquee").init({
        duration: 50,
        direction: "rtl",
        pauseOnHover: true,
        iterations: 2
    });
});