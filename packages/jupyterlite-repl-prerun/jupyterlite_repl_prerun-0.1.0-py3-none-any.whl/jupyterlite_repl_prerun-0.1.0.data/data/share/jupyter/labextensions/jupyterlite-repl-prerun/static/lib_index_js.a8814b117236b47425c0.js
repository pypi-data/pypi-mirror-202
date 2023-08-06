"use strict";
(self["webpackChunkjupyterlite_repl_prerun"] = self["webpackChunkjupyterlite_repl_prerun"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Initialization data for the jupyterlite-repl-prerun extension.
 */
const plugin = {
    id: 'jupyterlite-repl-prerun:plugin',
    autoStart: true,
    optional: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__.IConsoleTracker],
    activate: (app, tracker) => {
        if (!tracker) {
            return;
        }
        const search = window.location.search;
        const urlParams = new URLSearchParams(search);
        const prerun = urlParams.getAll('prerun');
        tracker.widgetAdded.connect(async (_, widget) => {
            const { console } = widget;
            if (prerun[0]) {
                await console.sessionContext.ready;
                prerun.forEach(line => { var _a, _b; return (_b = (_a = console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.requestExecute({
                    code: line,
                    silent: true,
                    store_history: false
                }); });
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.a8814b117236b47425c0.js.map