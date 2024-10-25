ckan.module("tweaks-select", function ($, _) {
    return {
        options: {
            selectId: null,
            selectOptions: null
        },
        initialize: function () {
            var select = this.$("#" + this.options.selectId);
            if (!select.length) {
                log.debug("Element with id #%s does not exist", this.options.selectId);
                return
            }

            var options = this.$("." + this.options.selectOptions);

            this.$(".pseudo-select-selected").text(
                select.find("option").eq(select[0].selectedIndex).text()
            );

            select.find("option").each(function (idx, el) {
                options.append(
                    $("<div>", {
                        text: el.textContent,
                        "data-index": idx,
                        "data-value": el.value,
                        "tabindex": '-1',
                        "class": select[0].selectedIndex === idx ? "active" : "",
                        "aria-label": el.textContent,
                        on: {
                            click: function () {
                                select[0].selectedIndex = idx;

                                if (select[0].form) {
                                    select[0].form.submit();
                                }
                            },
                            keypress: function(e) {
                                var key = e.which;
                                if(key == 13) {
                                    $(this).click();
                                }
                            },
                            keydown: function(e) {
                                let parent = $(this).parent();
                                let children = parent.children();
                                let next = (children.length - 1) == idx ? 0 : idx + 1;
                                let pre = idx - 1;
                                let key = e.which;

                                if(key == 38) {
                                    children.eq(pre).focus();
                                    e.preventDefault();
                                }
                                if(key == 40) {
                                    children.eq(next).focus();
                                    e.preventDefault();
                                }
                            }
                        },
                    })
                );
            });
        },
    };
});
