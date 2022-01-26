.. _tag_reference:

==================================================
Tag Reference
==================================================

| This reference describes the tags and their attributes provided by Nablarch.
| See :ref:`tag` for details on how to use each tag and examples of its use.

Form
 | :ref:`tag-form_tag` (form)

.. _tag_reference_input:

Enter
 | :ref:`tag-text_tag` (text)
 | :ref:`tag-search_tag` (search)
 | :ref:`tag-tel_tag` (tel)
 | :ref:`tag-url_tag` (URL)
 | :ref:`tag-email_tag` (email)
 | :ref:`tag-date_tag` (date)
 | :ref:`tag-month_tag` (month)
 | :ref:`tag-week_tag` (week)
 | :ref:`tag-time_tag` (time)
 | :ref:`tag-datetimeLocal_tag` (datetimeLocal)
 | :ref:`tag-number_tag` (number)
 | :ref:`tag-range_tag` (range)
 | :ref:`tag-color_tag` (color)
 | :ref:`tag-textarea_tag` (text area)
 | :ref:`tag-password_tag` (password)
 | :ref:`tag-radio_tag` (radio button)
 | :ref:`tag-checkbox_tag` (checkbox)
 | :ref:`tag-file_tag` (file)
 | :ref:`tag-plain_hidden_tag` (hidden)
 | :ref:`tag-select_tag` (pull-down)
 | :ref:`tag-composite_key_radio_button_tag` (radio button corresponding to the composite key)
 | :ref:`tag-composite_key_checkbox_tag` (checkbox corresponding to the composite key)
 | :ref:`tag-radio_buttons_tag` (multiple radio buttons)
 | :ref:`tag-checkboxes_tag` (multiple checkboxes)
 | :ref:`tag-code_select_tag` (code value pull-down)
 | :ref:`tag-code_checkbox_tag` (code value checkbox)
 | :ref:`tag-code_radio_buttons_tag` (multiple radio buttons for code values)
 | :ref:`tag-code_checkboxes_tag` (multiple checkboxes for code values)
 | :ref:`tag-hidden_tag` (hidden encryption)
 | :ref:`tag-hidden_store_tag` (hidden store)

.. _tag_reference_submit:

Submit
 Submit form
  | :ref:`tag-submit_tag` (button of input tag)
  | :ref:`tag-button_tag` (button of button tag)
  | :ref:`tag-submit_link_tag` (link)

 Open another window and submit (pop-up)
  | :ref:`tag-popup_submit_tag` (button of input tag)
  | :ref:`tag-popup_button_tag` (button of button tag)
  | :ref:`tag-popup_link_tag` (link)

 Submit for download
  | :ref:`tag-download_submit_tag` (button of input tag)
  | :ref:`tag-download_button_tag` (button of button tag)
  | :ref:`tag-download_link_tag` (link)

 Submit control
  | :ref:`tag-param_tag` (specification of parameter to be added during submission)
  | :ref:`tag-change_param_name_tag` (change parameter name when submitting for pop-up)

.. _tag_reference_output:

Output
 Value
  | :ref:`tag-write_tag` (object value)
  | :ref:`tag-pretty_print_tag` (object value. Do not perform escape only for qualified HTML (such as b tag))
  | :ref:`tag-raw_write_tag` (object value. Do not perform HTML escape)
  | :ref:`tag-code_tag` (code value)
 Message
  | :ref:`tag-message_tag` (message)
 Error
  | :ref:`tag-errors_tag` (list of error messages)
  | :ref:`tag-error_tag` (individual display of error messages)

HTML tag to specify URI (adding context path and URL rewrite)
 | :ref:`tag-a_tag`
 | :ref:`tag-img_tag`
 | :ref:`tag-link_tag`
 | :ref:`tag-script_tag`

Utility
 | :ref:`tag-no_cache_tag` (suppress browser cache)
 | :ref:`tag-set_tag` (configure a value to a variable)
 | :ref:`tag-include_tag` (include)
 | :ref:`tag-include_param_tag` (specification of parameters to be added for include)
 | :ref:`tag-confirmation_page_tag` (common input and confirmation screens)
 | :ref:`tag-ignore_confirmation_tag` (partially disable the screen state of the confirmation screen)
 | :ref:`tag-for_input_page_tag` (output body only on input screen)
 | :ref:`tag-for_confirmation_page_tag` (output body only on the confirmation screen)

Common attributes
========================
Refer to the common attributes defined here for each custom tag definition.

.. _tag-generic_attributes_tag:

All HTML tags
-------------------------

.. table::
   :class: tag-reference

   ============================= ==========================================================================================
   Attribute                     Description
   ============================= ==========================================================================================
   id                            XHTML id attribute.
   cssClass                      XHTML class attribute.
   style                         XHTML style attribute.
   title                         XHTML title attribute.
   lang                          XHTML lang attribute.
   xmlLang                       XHTML xml:lang attribute.
   dir                           XHTML dir attribute.
   onclick                       XHTML onclick attribute.
   ondblclick                    XHTML ondblclick attribute.
   onmousedown                   XHTML onmousedown attribute.
   onmouseup                     XHTML onmouseup attribute.
   onmouseover                   XHTML onmouseover attribute.
   onmousemove                   XHTML onmousemove attribute.
   onmouseout                    XHTML onmouseout attribute.
   onkeypress                    XHTML onkeypress attribute.
   onkeydown                     XHTML onkeydown attribute.
   onkeyup                       XHTML onkeyup attribute.
   ============================= ==========================================================================================

.. _tag-focus_attributes_tag:

HTML tags that can acquire focus
--------------------------------------------------

.. table::
   :class: tag-reference

   ============================= ==========================================================================================
   Attribute                     Description
   ============================= ==========================================================================================
   accesskey                     XHTML accesskey attribute.
   tabindex                      XHTML tabindex attribute.
   onfocus                       XHTML onfocus attribute.
   onblur                        XHTML onblur attribute.
   ============================= ==========================================================================================

.. _tag-dynamic_attributes_tag:

Using Dynamic Attributes
--------------------------------------------------

In tags that dynamic attributes are available, attributes that are not defined can also be set.

Individual attributes
======================================================

.. _tag-form_tag:

form tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   name                                   XHTML name attribute.
   action                                 XHTML action attribute.
   method                                 XHTML method attribute.
                                          Default is ``post``.
   enctype                                XHTML enctype attribute.
   onsubmit                               XHTML onsubmit attribute.
   onreset                                XHTML onreset attribute.
   accept                                 XHTML accept attribute.
   acceptCharset                          XHTML accept-charset attribute.
   target                                 XHTML target attribute.
   autocomplete                           HTML5 autocomplete attribute.
   windowScopePrefixes                    Window scope variable prefix.
                                          Use comma as a delimiter if more than one is specified.
                                          Outputs the request parameters that match the specified prefix as a hidden tag.
   useToken                               Whether to set up a token.
                                          ``True`` if the token is set, ``false`` if it is not set.
                                          Default is ``false``.
                                          If the :ref:`tag-confirmation_page_tag` is specified, it defaults to ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   preventPostResubmit                    Whether to use the POST retransmission prevention feature.
                                          Default is ``false``.
                                          ``True`` if used, ``false`` otherwise.
   ====================================== ==========================================================================================

.. _tag-text_tag:

text tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   readonly                               XHTML readonly attribute.
   size                                   XHTML size attribute.
   maxlength                              XHTML maxlength attribute.
   onselect                               XHTML onselect attribute.
   onchange                               XHTML onchange attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   placeholder                            HTML5 placeholder attribut.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-search_tag:

search tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-tel_tag:

tel tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-url_tag:

url tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-email_tag:

email tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-date_tag:

date tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-month_tag:

month tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-week_tag:

week tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-time_tag:

time tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-datetimeLocal_tag:

datetimeLocal tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-number_tag:

number tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-range_tag:

range tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-color_tag:

color tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   Attribute                              Description
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``required``                      XHTML name attribute. When displaying values, the value attribute is also used for the XHTML value attribute if no value attribute is specified.
   value                                  XHTML value attribute.
   disabled                               XHTML disabled attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   valueFormat                            Format for output.
                                          See :ref:`tag-format_value` for the specifics.
   ====================================== ====================================================================================================================

.. _tag-textarea_tag:

textarea tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   rows ``required``                      XHTML rows attribute.
   cols ``required``                      XHTML cols attribute.
   disabled                               XHTML disabled attribute.
   readonly                               XHTML readonly attribute.
   onselect                               XHTML onselect attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
   placeholder                            HTML5 placeholder attribute.
   maxlength                              HTML5 maxlength attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-password_tag:

password tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   disabled                               XHTML disabled attribute.
   readonly                               XHTML readonly attribute.
   size                                   XHTML size attribute.
   maxlength                              XHTML maxlength attribute.
   onselect                               XHTML onselect attribute.
   onchange                               XHTML onchange attribute.
   autocomplete                           HTML5 autocomplete attribute.
   autofocus                              HTML5 autofocus attribute.
   placeholder                            HTML5 placeholder attribute.
   restoreValue                           Whether to restore the input data when the input screen is redisplayed.
                                          ``True`` to restore, ``false`` to not restore.
                                          Default is ``false``.
   replacement                            Substitution characters to be used in the output for the confirmation screen.
                                          Default is ``*``.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-radio_tag:

radioButton tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   value ``required``                     XHTML value attribute.
   label ``required``                     Label.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-checkbox_tag:

checkbox tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   value                                  XHTML value attribute.
                                          The value used when there is a checkmark.
                                          Default is ``1``.
   autofocus                              HTML5 autofocus attribute.
   label                                  The label used when there is a checkmark.
                                          This label is displayed on the input screen.
   useOffValue                            Whether to use the value configuration without the checkmark.
                                          Default is ``true``.
   offLabel                               The label used when there is no checkmark.
   offValue                               The value used when there is no checkmark.
                                          Default is ``0``.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-composite_key_checkbox_tag:

compositeKeyCheckbox Tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   valueObject ``required``               Object used instead of the XHTML value attribute.
                                          Must have the property specified in the keyNames attribute.
   keyNames ``required``                  Key name of the composite key.
                                          Specify the key names using comma as the delimiter.
   namePrefix ``required``                Prefix to use when deploying to the request parameter.
                                          Unlike the normal name attribute, values that match the key name specified with ``.`` in this name and keyNames attribute are handled in the same way as normal name attributes. For example, if ``form`` is specified in the namePrefix attribute and ``key1`` and ``key2`` are specified in the keyNames attribute, the value of this checkbox will be output using the value included in the request scope with ``form.key1`` and ``form.key2`` during display. In addition, the value selected from the request parameters ``form.key1``, ``form.key2`` can be obtained in the process of the submitted request.
                                          The name attribute has a special restriction that it must have a name different from the key combination specified by the namePrefix and keyNames attributes. Pay attention to this point during implementation.
   autofocus                              HTML5 autofocus attribute.
   label                                  The label used when there is a checkmark.
                                          This label is displayed on the input screen.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-composite_key_radio_button_tag:

compositeKeyRadioButton tag
---------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   valueObject ``required``               Object used instead of the XHTML value attribute.
                                          Must have the property specified in the keyNames attribute.
   keyNames ``required``                  Key name of the composite key.
                                          Specify the key names using comma as the delimiter.
   namePrefix ``required``                Prefix to use when deploying to the request parameter.
                                          Unlike the normal name attribute, values that match the key name specified with ``.`` in this name and keyNames attribute are handled in the same way as normal name attributes. For example, if ``form`` is specified in the namePrefix attribute and ``key1`` and ``key2`` are specified in the keyNames attribute, the value of this checkbox will be output using the value included in the request scope with ``form.key1`` and ``form.key2`` during display. In addition, the value selected from the request parameters ``form.key1``, ``form.key2`` can be obtained in the process of the submitted request.
                                          The name attribute has a special restriction that it must have a name different from the key combination specified by the namePrefix and keyNames attributes. Pay attention to this point during implementation.
   autofocus                              HTML5 autofocus attribute.
   label                                  The label used when there is a checkmark.
                                          This label is displayed on the input screen.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-file_tag:

file tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   disabled                               XHTML disabled attribute.
   readonly                               XHTML readonly attribute.
   size                                   XHTML size attribute.
   maxlength                              XHTML maxlength attribute.
   onselect                               XHTML onselect attribute.
   onchange                               XHTML onchange attribute.
   accept                                 XHTML accept attribute.
   autofocus                              HTML5 autofocus attribute.
   multiple                               HTML5 multiple attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-hidden_tag:

hidden tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

Outputs value to the window scope without HTML tag output.

.. important::

  Window scope is deprecated.
  For details, see :ref:`tag-window_scope`.

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   disabled                               XHTML disabled attribute.
   ====================================== ==========================================================================================

.. _tag-plain_hidden_tag:

plainHidden tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   disabled                               XHTML disabled attribute.
   ====================================== ==========================================================================================

.. _tag-hidden_store_tag:

hiddenStore tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   disabled                               XHTML disabled attribute.
   ====================================== ==========================================================================================

.. _tag-select_tag:

select tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   Attribute                              Description
   ====================================== ======================================================================================================================
   :ref:`tag-generic_attributes_tag`
   name ``required``                      XHTML name attribute.
   listName ``required``                  Name of the option list.
                                          Custom tags use this name to acquire the option list from the request scope.
                                          If the option list acquired from the request scope is empty, nothing is displayed on the screen.
   elementLabelProperty ``required``      Property name to acquire the label from list element.
   elementValueProperty ``required``      Property name to acquire value from the list element.
   size                                   XHTML size attribute.
   multiple                               XHTML multiple attribute.
   disabled                               XHTML disabled attribute.
   tabindex                               XHTML tabindex attribute.
   onfocus                                XHTML onfocus attribute.
   onblur                                 XHTML onblur attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
   elementLabelPattern                    Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$LABEL$`` : Label
                                          ``$VALUE$`` : Value
                                          Default is ``$LABEL$`` .
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   withNoneOption                         Whether to add an unselected option to the top of the list.
                                          To add ``true``, not to add ``false``.
                                          Default is ``false``.
   noneOptionLabel                        Label to use for adding the not selected option to the top of the list.
                                          This attribute is valid only if ``true`` is specified for withNoneOption.
                                          Default is ``""``.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ======================================================================================================================

.. _tag-radio_buttons_tag:

radioButtons tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   Attribute                              Description
   ====================================== ======================================================================================================================
   :ref:`tag-generic_attributes_tag`      id attribute cannot be specified.
   :ref:`tag-focus_attributes_tag`        accesskey attribute cannot be specified.
   name ``required``                      XHTML name attribute.
   listName ``required``                  Name of the option list.
                                          Custom tags use this name to acquire the option list from the request scope.
                                          If the option list acquired from the request scope is empty, nothing is displayed on the screen.
   elementLabelProperty ``required``      Property name to acquire the label from list element.
   elementValueProperty ``required``      Property name to acquire value from the list element.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
                                          Output the autofocus attribute only for the first element among the options.
   elementLabelPattern                    Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$LABEL$`` : Label
                                          ``$VALUE$`` : Value
                                          Default is ``$LABEL$`` .
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ======================================================================================================================

.. _tag-checkboxes_tag:

checkbox tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id attribute cannot be specified.
   :ref:`tag-focus_attributes_tag`        accesskey attribute cannot be specified.
   name ``required``                      XHTML name attribute.
   listName ``required``                  Name of the option list.
                                          Custom tags use this name to acquire the option list from the request scope.
                                          If the option list acquired from the request scope is empty, nothing is displayed on the screen.
   elementLabelProperty ``required``      Property name to acquire the label from list element.
   elementValueProperty ``required``      Property name to acquire value from the list element.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
                                          Output the autofocus attribute only for the first element among the options.
   elementLabelPattern                    Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$LABEL$`` : Label
                                          ``$VALUE$`` : Value
                                          Default is ``$LABEL$`` .
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-submit_tag:

submit tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   type ``required``                      XHTML type attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   disabled                               XHTML disabled attribute.
   value                                  XHTML value attribute.
   src                                    XHTML src attribute.
   alt                                    XHTML alt attribute.
   usemap                                 XHTML usemap attribute.
   align                                  XHTML align attribute.
   autofocus                              HTML5 autofocus attribute.
   allowDoubleSubmission                  Whether to allow double submission.
                                          Configure to ``true`` when allowed and to ``false`` when not allowed.
                                          Default is ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-button_tag:

button tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   value                                  XHTML value attribute.
   type                                   XHTML type attribute.
   disabled                               XHTML disabled attribute.
   autofocus                              HTML5 autofocus attribute.
   allowDoubleSubmission                  Whether to allow double submission.
                                          Configure to ``true`` when allowed and to ``false`` when not allowed.
                                          Default is ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-submit_link_tag:

submitLink tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   shape                                  XHTML shape attribute.
   coords                                 XHTML coords attribute.
   allowDoubleSubmission                  Whether to allow double submission.
                                          Configure to ``true`` when allowed and to ``false`` when not allowed.
                                          Default is ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-popup_submit_tag:

popupSubmit tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   type ``required``                      XHTML type attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   disabled                               XHTML disabled attribute.
   value                                  XHTML value attribute.
   src                                    XHTML src attribute.
   alt                                    XHTML alt attribute.
   usemap                                 XHTML usemap attribute.
   align                                  XHTML align attribute.
   autofocus                              HTML5 autofocus attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   popupWindowName                        Window name of pop-up.
                                          Specify the second argument (JavaScript) of the window.open function when opening a new window.
   popupOption                            Pop-up option information.
                                          Specify the third argument (JavaScript) of the window.open function when opening a new window.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-popup_button_tag:

popupButton tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   value                                  XHTML value attribute.
   type                                   XHTML type attribute.
   disabled                               XHTML disabled attribute.
   autofocus                              HTML5 autofocus attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   popupWindowName                        Window name of pop-up.
                                          Specify the second argument (JavaScript) of the window.open function when opening a new window.
   popupOption                            Pop-up option information.
                                          Specify the third argument (JavaScript) of the window.open function when opening a new window.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-popup_link_tag:

popupLink tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   shape                                  XHTML shape attribute.
   coords                                 XHTML coords attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   popupWindowName                        Window name of pop-up.
                                          Specify the second argument (JavaScript) of the window.open function when opening a new window.
   popupOption                            Pop-up option information.
                                          Specify the third argument (JavaScript) of the window.open function when opening a new window.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-download_submit_tag:

downloadSubmit tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   type ``required``                      XHTML type attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   disabled                               XHTML disabled attribute.
   value                                  XHTML value attribute.
   src                                    XHTML src attribute.
   alt                                    XHTML alt attribute.
   usemap                                 XHTML usemap attribute.
   align                                  XHTML align attribute.
   autofocus                              HTML5 autofocus attribute.
   allowDoubleSubmission                  Whether to allow double submission.
                                          Configure to ``true`` when allowed and to ``false`` when not allowed.
                                          Default is ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-download_button_tag:

downloadButton tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   value                                  XHTML value attribute.
   type                                   XHTML type attribute.
   disabled                               XHTML disabled attribute.
   autofocus                              HTML5 autofocus attribute.
   allowDoubleSubmission                  Whether to allow double submission.
                                          Configure to ``true`` when allowed and to ``false`` when not allowed.
                                          Default is ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-download_link_tag:

downloadLink tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name                                   XHTML name attribute.
   uri ``required``                       URI.
                                          See :ref:`tag-specify_uri`.
   shape                                  XHTML shape attribute.
   coords                                 XHTML coords attribute.
   allowDoubleSubmission                  Whether to allow double submission.
                                          Configure to ``true`` when allowed and to ``false`` when not allowed.
                                          Default is ``true``.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   displayMethod                          A display method in the case of performing display control based on the result of authorization determination and service availability determination.
                                          Specify one of the following.
                                          NODISPLAY (no display)
                                          DISABLED (disabled)
                                          NORMAL (normal display)
   ====================================== ==========================================================================================

.. _tag-param_tag:

param tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   paramName ``required``                 Name of the parameter to use for submission.
   name                                   The name to acquire the value.
                                          Specify for referring to objects in the scope such as the request scope.
                                          Specify either name attribute or value attribute.
   value                                  Value.
                                          Used to specify a value directly.
                                          Specify either name attribute or value attribute.
   ====================================== ==========================================================================================

.. _tag-change_param_name_tag:

changeParamName tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   paramName ``required``                 Name of the parameter to use for submission.
   inputName ``required``                 Name attribute of the input element of the source screen to be changed.
   ====================================== ==========================================================================================

.. _tag-a_tag:

a tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   charset                                XHTML charset attribute.
   type                                   XHTML type attribute.
   name                                   XHTML name attribute.
   href                                   XHTML href attribute.
                                          See :ref:`tag-specify_uri`.
   hreflang                               XHTML hreflang attribute.
   rel                                    XHTML rel attribute.
   rev                                    XHTML rev attribute.
   shape                                  XHTML shape attribute.
   coords                                 XHTML coords attribute.
   target                                 XHTML target attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   ====================================== ==========================================================================================

.. _tag-img_tag:

img tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   src ``required``                       XHTML charsrc attribute.
                                          See :ref:`tag-specify_uri`.
   alt ``required``                       XHTML alt attribute.
   name                                   XHTML name attribute.
   longdesc                               XHTML longdesc attribute.
   height                                 XHTML height attribute.
   width                                  XHTML width attribute.
   usemap                                 XHTML usemap attribute.
   ismap                                  XHTML ismap attribute.
   align                                  XHTML align attribute.
   border                                 XHTML border attribute.
   hspace                                 XHTML hspace attribute.
   vspace                                 XHTML vspace attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   ====================================== ==========================================================================================

.. _tag-link_tag:

link tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   charset                                XHTML charset attribute.
   href                                   XHTML href attribute.
                                          See :ref:`tag-specify_uri`.
   hreflang                               XHTML hreflang attribute.
   type                                   XHTML type attribute.
   rel                                    XHTML rel attribute.
   rev                                    XHTML rev attribute.
   media                                  XHTML media attribute.
   target                                 XHTML target attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   ====================================== ==========================================================================================

.. _tag-script_tag:

script tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   type ``required``                      XHTML type attribute.
   id                                     XHTML id attribute.
   charset                                XHTML charset attribute.
   language                               XHTML language attribute.
   src                                    XHTML src attribute.
                                          See :ref:`tag-specify_uri`.
   defer                                  XHTML defer attribute.
   xmlSpace                               XHTML xml:space attribute.
   secure                                 Whether to use https for URI.
                                          To use https ``true``, not to use https ``false``.
   ====================================== ==========================================================================================

.. _tag-errors_tag:

errors tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== =================================================================================================
   Attribute                              Description
   ====================================== =================================================================================================
   cssClass                               CSS class name to use for ul tags in the list display.
                                          Default is ``nablarch_errors``.
   infoCss                                CSS class name used for information-level messages.
                                          Default is ``nablarch_info``.
   warnCss                                CSS class name used for warning-level messages.
                                          Default is ``nablarch_warn``.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   filter                                 Filter criteria for messages to be included in the list.
                                          Specify one of the following.
                                          all (display all messages)
                                          global (display only messages not corresponding to input items)
                                          Default is ``all``.
                                          For global, the message containing the property name of :java:extdoc:`ValidationResultMessage<nablarch.core.validation.ValidationResultMessage>` is removed and output.
   ====================================== =================================================================================================

.. _tag-error_tag:

error tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   name ``required``                      The name attribute of the input item that displays the error message.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   messageFormat                          Format used to display the message.
                                          Specify one of the following.
                                          div (div tag)
                                          span (span tag)
                                          Default is ``div``.
   ====================================== ==========================================================================================

.. _tag-no_cache_tag:

noCache tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

No attribute.

.. _tag-code_select_tag:

codeSelect tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   name ``required``                      XHTML name attribute.
   codeId ``required``                    Code ID.
   size                                   XHTML size attribute.
   multiple                               XHTML multiple attribute.
   disabled                               XHTML disabled attribute.
   tabindex                               XHTML tabindex attribute.
   onfocus                                XHTML onfocus attribute.
   onblur                                 XHTML onblur attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
   pattern                                Column name of the pattern used.
                                          Default is not specified.
   optionColumnName                       Column name of option name to acquire.
   labelPattern                           Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$NAME$``: Code name corresponding to the code value
                                          ``$SHORTNAME$``: Abbreviation of code corresponding to the code value
                                          ``$OPTIONALNAME$``: Option name of code corresponding to the code value
                                          ``$VALUE$``: Code value
                                          ``$OPTIONALNAME$`` is used, specifying the optionColumnName attribute is required.
                                          Default is ``$NAME$``.
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   withNoneOption                         Whether to add an unselected option to the top of the list.
                                          To add ``true``, not to add ``false``.
                                          Default is ``false``.
   noneOptionLabel                        Label to use for adding the not selected option to the top of the list.
                                          This attribute is valid only if ``true`` is specified for withNoneOption.
                                          Default is ``""``.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================


.. _tag-code_radio_buttons_tag:

codeRadioButtons tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id attribute cannot be specified.
   :ref:`tag-focus_attributes_tag`        accesskey attribute cannot be specified.
   name ``required``                      XHTML name attribute.
   codeId ``required``                    Code ID.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
                                          Output the autofocus attribute only for the first element among the options.
   pattern                                Column name of the pattern used.
                                          Default is not specified.
   optionColumnName                       Column name of option name to acquire.
   labelPattern                           Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$NAME$``: Code name corresponding to the code value
                                          ``$SHORTNAME$``: Abbreviation of code corresponding to the code value
                                          ``$OPTIONALNAME$``: Option name of code corresponding to the code value
                                          ``$VALUE$``: Code value
                                          ``$OPTIONALNAME$`` is used, specifying the optionColumnName attribute is required.
                                          Default is ``$NAME$``.
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-code_checkboxes_tag:

codeCheckboxes tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id attribute cannot be specified.
   :ref:`tag-focus_attributes_tag`        accesskey attribute cannot be specified.
   name ``required``                      XHTML name attribute.
   codeId ``required``                    Code ID.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   autofocus                              HTML5 autofocus attribute.
                                          Output the autofocus attribute only for the first element among the options.
   pattern                                Column name of the pattern used.
                                          Default is not specified.
   optionColumnName                       Column name of option name to acquire.
   labelPattern                           Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$NAME$``: Code name corresponding to the code value
                                          ``$SHORTNAME$``: Abbreviation of code corresponding to the code value
                                          ``$OPTIONALNAME$``: Option name of code corresponding to the code value
                                          ``$VALUE$``: Code value
                                          ``$OPTIONALNAME$`` is used, specifying the optionColumnName attribute is required.
                                          Default is ``$NAME$``.
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-code_checkbox_tag:

codeCheckbox tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``required``                      XHTML name attribute.
   value                                  XHTML value attribute.
                                          The code value used when there is a checkmark.
                                          Default is ``1``.
   autofocus                              HTML5 autofocus attribute.
   codeId ``required``                    Code ID.
   optionColumnName                       Column name of option name to acquire.
   labelPattern                           Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$NAME$``: Code name corresponding to the code value
                                          ``$SHORTNAME$``: Abbreviation of code corresponding to the code value
                                          ``$OPTIONALNAME$``: Option name of code corresponding to the code value
                                          ``$VALUE$``: Code value
                                          ``$OPTIONALNAME$`` is used, specifying the optionColumnName attribute is required.
                                          Default is ``$NAME$``.
   offCodeValue                           The code value used when there is no checkmark.
                                          If the offCodeValue attribute is not specified,
                                          search for the code value to use if there is no check from the value of the codeId attribute.
                                          If there are 2 search results and one is the value of the value attribute,
                                          use the remaining as a code value without check.
                                          If not found with the search, use the default value ``0``.
   disabled                               XHTML disabled attribute.
   onchange                               XHTML onchange attribute.
   errorCss                               CSS class name used for error level messages.
                                          Default is ``nablarch_error``.
   nameAlias                              Configure alias of name attribute.
                                          Use comma as a delimiter if more than one is specified.
   ====================================== ==========================================================================================

.. _tag-code_tag:

code tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Available

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   name                                   Name used to acquire the code value to be displayed from the variable scope.
                                          if omitted, a list of codes filtered down by the code ID attribute and pattern attribute is displayed.
   codeId ``required``                    Code ID.
   pattern                                Column name of the pattern used.
                                          Default is not specified.
   optionColumnName                       Column name of option name to acquire.
   labelPattern                           Pattern to format the label.
                                          Placeholders are shown below.
                                          ``$NAME$``: Code name corresponding to the code value
                                          ``$SHORTNAME$``: Abbreviation of code corresponding to the code value
                                          ``$OPTIONALNAME$``: Option name of code corresponding to the code value
                                          ``$VALUE$``: Code value
                                          ``$OPTIONALNAME$`` is used, specifying the optionColumnName attribute is required.
                                          Default is ``$NAME$``.
   listFormat                             Format to use when displaying the list.
                                          Specify one of the following.
                                          br(br tag)
                                          div(div tag)
                                          span(span tag)
                                          ul(ul tag)
                                          ol(ol tag)
                                          sp(space delimited)
                                          Default is br.
   ====================================== ==========================================================================================

.. _tag-message_tag:

message tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ===============================================================================================
   Attribute                              Description
   ====================================== ===============================================================================================
   messageId ``required``                 Message ID.
   option0 ~ option9                      Optional arguments with index between 0 ~ 9 used for message format.
                                          Up to 10 optional arguments can be specified.
   language                               Language of the message.
                                          The language configured in the thread context is the default.
   var                                    Variable name used when storing in the request scope.
                                          If var attribute is specified, configures in the request scope without output of a message.
                                          HTML escape and HTML format are not performed when configuring in the request scope.
   htmlEscape                             Whether HTML escape is to be performed.
                                          To perform HTML escape ``true``, not to perform HTML escape ``false``.
                                          Default is ``true``.
   withHtmlFormat                         Whether to use the HTML format (conversion of carriage return and line feed and half-width).
                                          HTML format is valid only when HTML escape is used.
                                          Default is ``true``.
   ====================================== ===============================================================================================

.. _tag-write_tag:

write tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   Attribute                              Description
   ====================================== ======================================================================================================================
   name                                   Name used to acquire the value to be displayed from the variable scope. Cannot be specified at the same time as the value attribute.
   value                                  Value to be displayed.Used to specify a value directly. Cannot be specified at the same time as the name attribute.
   withHtmlFormat                         Whether to use the HTML format (conversion of carriage return and line feed and half-width).
                                          HTML format is valid only when HTML escape is used.
                                          Default is ``true``.
   valueFormat                            Format used for output.
                                          For the contents to be specified, see :ref:`tag-format_value`.
   ====================================== ======================================================================================================================


.. _tag-pretty_print_tag:

prettyPrint tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. important::

  This tag is deprecated and should not be used.
  For details, see :ref:`reason why the use of prettyPrint tag is not recommended <tag-pretty_print_tag-deprecated>`.

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   name ``required``                      Name used to acquire the value to be displayed from the variable scope
   ====================================== ==========================================================================================



.. _tag-raw_write_tag:

rawWrite tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   name ``required``                      Name used to acquire the value to be displayed from the variable scope
   ====================================== ==========================================================================================


.. _tag-set_tag:

set tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   var ``required``                       Variable name used when storing in the request scope.
   name                                   The name to acquire the value. Specify either name attribute or value attribute.
   value                                  Value. Used to specify a value directly.Specify either name attribute or value attribute.
   scope                                  Configure the scope for storing variables.
                                          Scope that can be specified is given below.
                                          page: Page scope.
                                          request: Request scope.
                                          Default is request scope.
   bySingleValue                          Whether to acquire the value corresponding to the name attribute as a single value.
                                          Default is ``true``.
   ====================================== ==========================================================================================

.. _tag-include_tag:

include tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   path ``required``                      Path of the resource to include.
   ====================================== ==========================================================================================

.. _tag-include_param_tag:

includeParam tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   paramName ``required``                 Name of the parameter to use for include.
   name                                   The name to acquire the value. Specify either name attribute or value attribute.
   value                                  Value. Used to specify a value directly.Specify either name attribute or value attribute.
   ====================================== ==========================================================================================

.. _tag-confirmation_page_tag:

confirmationPage tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   Attribute                              Description
   ====================================== ==========================================================================================
   path                                   Path of the forward destination (input screen).
   ====================================== ==========================================================================================

.. _tag-ignore_confirmation_tag:

ignoreConfirmation tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

No attribute.

.. _tag-for_input_page_tag:

forInputPage tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

No attribute.

.. _tag-for_confirmation_page_tag:

forConfirmationPage tag
-------------------------

:ref:`Availability of dynamic attributes <tag-dynamic_attributes_tag>` ：Unavailable

No attribute.
