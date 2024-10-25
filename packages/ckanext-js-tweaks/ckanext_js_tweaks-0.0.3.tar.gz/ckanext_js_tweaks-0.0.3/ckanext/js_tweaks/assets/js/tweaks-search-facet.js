ckan.module("tweaks-search-facet", function () {
    "use strict";
    return {
        initialize: function () {
            this._hideChildren = this._hideChildren.bind(this);
            this._onInputChange = this._onInputChange.bind(this);
            this._checkForHiddenness = this._checkForHiddenness.bind(this);
            this._deleteEmptyEl = this._deleteEmptyEl.bind(this);

            this.ulElement = this.el[0].nextElementSibling;
            this.children = this.ulElement.querySelectorAll("li");

            this.el[0].addEventListener("input", this._onInputChange);
            this._hideChildren();
        },
        _checkForHiddenness: function () {
            if (this._isAllHidden(this.children)) {
                if (this.ulElement.querySelector("p.empty")) {
                    return;
                }
                const emptyEl = document.createElement("p");
                emptyEl.classList.add("module-content", "empty");
                emptyEl.textContent = "No options found. Please try another search.";
                this.ulElement.appendChild(emptyEl);
            } else {
                this._deleteEmptyEl();
            }
        },
        _isAllHidden: function (children) {
            for (var i = 0; i < children.length; i++) {
                if (!children[i].hidden) {
                    return false;
                }
            }
            return true;
        },
        _deleteEmptyEl: function () {
            const emptyEl = this.ulElement.querySelector("p.empty");
            if (emptyEl) emptyEl.remove();
        },
        _onInputChange: function (e) {
            const val = e.target.value.toLowerCase();

            for (var i = 0; i < this.children.length; i++) {
                this.children[i].hidden = !~(
                    this.children[i]
                        .querySelector(".item-label")
                        .textContent.toLowerCase() || ""
                ).indexOf(val);
            }

            this._hideChildren();
        },
        _hideChildren: function () {
            // show only first 10 not hidden children
            for (var i = 0, shownItems = 0; i < this.children.length; i++) {
                if (!this.children[i].hidden) shownItems++;
                if (shownItems > 10) this.children[i].hidden = true;
            }
            this._checkForHiddenness();
        },
    };
});
