.. _normalize_handler:

Normalize Handler
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

This handler normalizes the request parameters sent by the client.

This handler performs the following process.

* Normalization process of request parameter

The process flow is as follows.

.. image:: ../images/NormalizationHandler/flow.png
  :scale: 75

Handler class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.NormalizationHandler`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

Constraints
------------------------------
Place this handler after the :ref:`multipart_handler`
  This handler accesses the request parameters.
  Therefore, this handler must be configured after the :ref:`multipart_handler`.

Normalization process provided as standard
--------------------------------------------------
The following normalization process is provided as standard.

* Normalizer that removes white space before and after the request parameter ( :java:extdoc:`TrimNormalizer <nablarch.fw.web.handler.normalizer.TrimNormalizer>` ) [#whitespace]_


Add the normalization process
--------------------------------------------------
This handler is the default action, and the normalizer that removes the white space [#whitespace]_ before and after the request parameter is enabled.

When the normalization process is added to the project requirements, create an implementation class :java:extdoc:`Normalizer <nablarch.fw.web.handler.normalizer.Normalizer>` and configure in this handler.

An example is shown below.

Implementation example of normalizer
  .. code-block:: java

    public class SampleNormalizer implements Normalizer {

        @Override
        public boolean canNormalize(final String key) {
          // If num is included in the key value of the parameter, normalize the parameter
          return key.contains("num");
        }

        @Override
        public String[] normalize(final String[] value) {
          // Remove the comma (,) in the parameter
          final String[] result = new String[value.length];
          for (int i = 0; i < value.length; i++) {
              result[i] = value[i].replace(",", "");
          }
          return result;
        }
    }

Define in the component configuration file
  Configure the normalizer to be applied as shown in the following configuration example.
  When multiple normalizers are configured, the normalizing process is executed sequentially from the one configured higher.
  Therefore, if the normalization process has order, pay attention to the configuration order.

  .. code-block:: xml

    <component class="nablarch.fw.web.handler.NormalizationHandler">
      <property name="normalizers">
        <list>
          <component class="sample.SampleNormalizer" />
          <component class="nablarch.fw.web.handler.normalizer.TrimNormalizer" />
        </list>
      </property>
    </component>

.. tip::
  When the handler is configured as follows without configuring the normalizer, a normalizer that removes the leading and trailing whitespace provided by default is automatically applied.

  .. code-block:: xml

    <component class="nablarch.fw.web.handler.NormalizationHandler" />


.. [#whitespace] For the definition of whitespace, see :java:extdoc:`Character#isWhitespace <java.lang.Character.isWhitespace(int)>`
