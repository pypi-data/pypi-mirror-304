/*global SelectBox, interpolate*/
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.
'use strict';
{
    const $ = django.jQuery;
    let popupIndex = 0;
    const relatedWindows = [];

    function dismissChildPopups() {
        relatedWindows.forEach(function (win) {
            if (!win.closed) {
                win.dismissChildPopups();
                win.close();
            }
        });
    }

    function setPopupIndex() {
        if (document.getElementsByName("_popup").length > 0) {
            const index = window.name.lastIndexOf("__") + 2;
            popupIndex = parseInt(window.name.substring(index));
        } else {
            popupIndex = 0;
        }
    }

    function addPopupIndex(name) {
        return name + "__" + (popupIndex + 1);
    }

    function removePopupIndex(name) {
        return name.replace(new RegExp("__" + (popupIndex + 1) + "$"), '');
    }

    function showAdminPopup(triggeringLink, name_regexp, add_popup) {
        $('#generalModal .modal-box').html(
            `<button class="btn"><span class="loading loading-spinner"></span>loading</button>`
        );
        const name = addPopupIndex(triggeringLink.id.replace(name_regexp, ''));
        const href = new URL(triggeringLink.href);
        if (add_popup) {
            href.searchParams.set('_popup', 1);
        }

        $.ajax({
            url: href, // The URL of the page you're requesting
            type: 'GET', // The request method (can be GET, POST, etc.)
            success: function (response) {
                // What to do if the request is successful
                var iframe = $('<iframe>', {
                    id: 'myIframe',
                    frameborder: 0,
                    width: '100%',
                    height: '100%'
                });

                // Append the iframe to your container
                $('#generalModal .modal-box').html(iframe);

                // Write the response to the iframe's document
                var iframeDoc = iframe[0].contentDocument || iframe[0].contentWindow.document;
                iframeDoc.open();
                iframeDoc.write(response);
                iframeDoc.close();
                // You can manipulate the response or update the DOM here
            },
            error: function (error) {
                // What to do if the request fails
                console.log('Error:', error);
            }
        });


        document.getElementById('generalModal').showModal()

        // const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
        // relatedWindows.push(win);
        // win.focus();
        return false;
    }

    function showRelatedObjectLookupPopup(triggeringLink) {
        return showAdminPopup(triggeringLink, /^lookup_/, true);
    }

    function dismissRelatedLookupPopup(win, chosenId) {
        const name = removePopupIndex(win.name);
        const elem = document.getElementById(name);
        if (elem.classList.contains('vManyToManyRawIdAdminField') && elem.value) {
            elem.value += ',' + chosenId;
        } else {
            document.getElementById(name).value = chosenId;
        }
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    function showRelatedObjectPopup(triggeringLink) {
        return showAdminPopup(triggeringLink, /^(change|add|delete)_/, false);
    }

    function updateRelatedObjectLinks(triggeringLink) {
        const $this = $(triggeringLink);
        const siblings = $this.parents('.related-widget-wrapper').find('.view-related, .change-related, .delete-related');
        if (!siblings.length) {
            return;
        }
        const value = $this.val();
        if (value) {
            siblings.each(function () {
                const elm = $(this);
                elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
                elm.removeAttr('aria-disabled');
            });
        } else {
            siblings.removeAttr('href');
            siblings.attr('aria-disabled', true);
        }
    }

    function updateRelatedSelectsOptions(currentSelect, win, objId, newRepr, newId) {
        // After create/edit a model from the options next to the current
        // select (+ or :pencil:) update ForeignKey PK of the rest of selects
        // in the page.

        const path = win.location.pathname;
        // Extract the model from the popup url '.../<model>/add/' or
        // '.../<model>/<id>/change/' depending the action (add or change).
        const modelName = path.split('/')[path.split('/').length - (objId ? 4 : 3)];
        // Exclude autocomplete selects.
        const selectsRelated = document.querySelectorAll(`[data-model-ref="${modelName}"] select:not(.admin-autocomplete)`);

        selectsRelated.forEach(function (select) {
            if (currentSelect === select) {
                return;
            }

            let option = select.querySelector(`option[value="${objId}"]`);

            if (!option) {
                option = new Option(newRepr, newId);
                select.options.add(option);
                return;
            }

            option.textContent = newRepr;
            option.value = newId;
        });
    }

    function dismissAddRelatedObjectPopup(win, newId, newRepr) {
        const name = removePopupIndex(win.name);
        const elem = document.getElementById(name);
        if (elem) {
            const elemName = elem.nodeName.toUpperCase();
            if (elemName === 'SELECT') {
                elem.options[elem.options.length] = new Option(newRepr, newId, true, true);
                updateRelatedSelectsOptions(elem, win, null, newRepr, newId);
            } else if (elemName === 'INPUT') {
                if (elem.classList.contains('vManyToManyRawIdAdminField') && elem.value) {
                    elem.value += ',' + newId;
                } else {
                    elem.value = newId;
                }
            }
            // Trigger a change event to update related links if required.
            $(elem).trigger('change');
        } else {
            const toId = name + "_to";
            const o = new Option(newRepr, newId);
            SelectBox.add_to_cache(toId, o);
            SelectBox.redisplay(toId);
        }
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    function dismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
        const id = removePopupIndex(win.name.replace(/^edit_/, ''));
        const selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
        const selects = $(selectsSelector);
        selects.find('option').each(function () {
            if (this.value === objId) {
                this.textContent = newRepr;
                this.value = newId;
            }
        }).trigger('change');
        updateRelatedSelectsOptions(selects[0], win, objId, newRepr, newId);
        selects.next().find('.select2-selection__rendered').each(function () {
            // The element can have a clear button as a child.
            // Use the lastChild to modify only the displayed value.
            this.lastChild.textContent = newRepr;
            this.title = newRepr;
        });
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    function dismissDeleteRelatedObjectPopup(win, objId) {
        const id = removePopupIndex(win.name.replace(/^delete_/, ''));
        const selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
        const selects = $(selectsSelector);
        selects.find('option').each(function () {
            if (this.value === objId) {
                $(this).remove();
            }
        }).trigger('change');
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    window.showRelatedObjectLookupPopup = showRelatedObjectLookupPopup;
    window.dismissRelatedLookupPopup = dismissRelatedLookupPopup;
    window.showRelatedObjectPopup = showRelatedObjectPopup;
    window.updateRelatedObjectLinks = updateRelatedObjectLinks;
    window.dismissAddRelatedObjectPopup = dismissAddRelatedObjectPopup;
    window.dismissChangeRelatedObjectPopup = dismissChangeRelatedObjectPopup;
    window.dismissDeleteRelatedObjectPopup = dismissDeleteRelatedObjectPopup;
    window.dismissChildPopups = dismissChildPopups;

    // Kept for backward compatibility
    window.showAddAnotherPopup = showRelatedObjectPopup;
    window.dismissAddAnotherPopup = dismissAddRelatedObjectPopup;

    window.addEventListener('unload', function (evt) {
        window.dismissChildPopups();
    });

    $(document).ready(function () {
        setPopupIndex();
        $("a[data-popup-opener]").on('click', function (event) {
            event.preventDefault();
            opener.dismissRelatedLookupPopup(window, $(this).data("popup-opener"));
        });
        $('body').on('click', '.related-widget-wrapper-link[data-popup="yes"]', function (e) {
            e.preventDefault();
            if (this.href) {
                const event = $.Event('django:show-related', {href: this.href});
                $(this).trigger(event);
                if (!event.isDefaultPrevented()) {
                    showRelatedObjectPopup(this);
                }
            }
        });
        $('body').on('change', '.related-widget-wrapper select', function (e) {
            const event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                updateRelatedObjectLinks(this);
            }
        });
        $('.related-widget-wrapper select').trigger('change');
        $('body').on('click', '.related-lookup', function (e) {
            e.preventDefault();
            const event = $.Event('django:lookup-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showRelatedObjectLookupPopup(this);
            }
        });
    });
}
