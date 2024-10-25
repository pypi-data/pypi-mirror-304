ckan.module("tweaks-show-more", function () {
    "use strict";

    return {
        initialize: function () {
            this._clickShowMore = this._clickShowMore.bind(this);
            this._showAllElements = this._showAllElements.bind(this);
            this._hideElements = this._hideElements.bind(this);

            this.el[0].addEventListener("click", this._clickShowMore);
            this.listItems = this.el[0].parentElement.previousElementSibling.querySelectorAll(
                "ul li"
            );

            if (this.listItems.length > 10) {
                this._hideElements();
            } else {
                this.el[0].remove();
            }
        },
        _hideElements: function () {
            for (var i = 10; i < this.listItems.length; i++) {
                this.listItems[i].hidden = true;
            }
        },
        _clickShowMore: function (e) {
            if (this.expanded) {
                this._hideElements();
                this.expanded = false;
                e.target.textContent = e.target.textContent.replace("Less", "More");
            } else {
                this._showAllElements();
                this.expanded = true;
                e.target.textContent = e.target.textContent.replace("More", "Less");
            }
        },
        _showAllElements: function () {
            for (var i = 0; i < this.listItems.length; i++) {
                this.listItems[i].hidden = false;
            }
        },
    };
});
