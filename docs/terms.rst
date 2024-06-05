========================
Terms used in the schema
========================

Contents
========
.. contents::

Document Sections
=================

turbine
-------

General information about the physical turbine and its default
operational values

turbine.manufacturer_name
~~~~~~~~~~~~~~~~~~~~~~~~~

Full name of the manufacturer (eg a legal entity)

Examples:

.. code-block:: js

   "Generic Turbines (US) Inc."

turbine.manufacturer_display_name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shortened or informal name of the manufacturer (for display purposes, eg
in dropdown selectors). See also manufacturer_name.

Examples:

.. code-block:: js

   "Generic Turbines"

turbine.model_name
~~~~~~~~~~~~~~~~~~

Name of the turbine model as stated on the Type Certificate, Design
Evaluation Confirmity Statement or Statement of Compliance.

Examples:

.. code-block:: js

   "GT101"

turbine.model_description
~~~~~~~~~~~~~~~~~~~~~~~~~

General description about the turbine model, eg for giving a brief
overview in a turbine selection tool.

Examples:

.. code-block:: js

   "An example simple turbine with only one mode."

turbine.platform_name
~~~~~~~~~~~~~~~~~~~~~

Optional name of the platform on which this turbine model is based.

Examples:

.. code-block:: js

   "1.x Series"

turbine.platform_description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optional general description of the platform on which this turbine model
is based.

Examples:

.. code-block:: js

   "The 1.x Series platform was designed as a basis for a range of small-scale onshore turbines versatile for a range of site conditions."

turbine.rotor_diameter
~~~~~~~~~~~~~~~~~~~~~~

Nominal rotor diameter of the turbine [m]

Examples:

.. code-block:: js

   100.0

turbine.number_of_blades
~~~~~~~~~~~~~~~~~~~~~~~~

The number of blades (typically 3, occasionally 2)

Examples:

.. code-block:: js

   3

.. code-block:: js

   2

turbine.drive_type
~~~~~~~~~~~~~~~~~~

The drive type of the turbine

turbine.regulation_type
~~~~~~~~~~~~~~~~~~~~~~~

The regulation type of the turbine.

turbine.rated_power
~~~~~~~~~~~~~~~~~~~

turbine.cut_in_rpm
~~~~~~~~~~~~~~~~~~

turbine.available_hub_heights
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

turbine.grid_frequencies
~~~~~~~~~~~~~~~~~~~~~~~~

design_bases
------------

A list of design bases for turbine certification or describing
site-specific environmental conditions. Each contains information about
the design point (environmental conditions) for which the power curves
in this document are intended.

design_bases.label
~~~~~~~~~~~~~~~~~~

A string key identifying the design basis, eg `my_design_basis_1`

Examples:

.. code-block:: js

   "basis_1"

.. code-block:: js

   "basis_2"

.. code-block:: js

   "site_xyz_specific"

design_bases.name
~~~~~~~~~~~~~~~~~

A human-readable name matching this basis label (eg for use in UIs)

Examples:

.. code-block:: js

   "Basis 1"

.. code-block:: js

   "Basis 2"

.. code-block:: js

   "Site XYZ Specific"

design_bases.certification
~~~~~~~~~~~~~~~~~~~~~~~~~~

Information about the scheme under which this design basis was
certified. This is not a required property, so if a turbine is as-yet
uncertified, simply leave it out.

Examples:

.. code-block:: js

   {
       "certificate_reference": "IECRE.WE.TC.20.0099-R6",
       "standard": "IEC",
       "standard_edition": "2"
   }

design_bases.certification.certificate_reference
++++++++++++++++++++++++++++++++++++++++++++++++

Identifies the certificate associated with the power curve. Note that
multiple design bases may refer to the same certificate.

Examples:

.. code-block:: js

   "44 220 15454566-D-IEC Rev. 4"

.. code-block:: js

   "IECRE.WE.TC.86.0179-R6"

design_bases.certification.standard
+++++++++++++++++++++++++++++++++++

The certification scheme under which the power curves were certified.

design_bases.certification.standard_edition
+++++++++++++++++++++++++++++++++++++++++++

The edition of the standard used in turbine certification

design_bases.design_class
~~~~~~~~~~~~~~~~~~~~~~~~~

A fully or partially predefined environmental class, (eg IEC or other
scheme)

design_bases.design_class[0].class_label
++++++++++++++++++++++++++++++++++++++++

Select from predefined IEC design classes I, II, and III.

design_bases.design_class[1].class_label
++++++++++++++++++++++++++++++++++++++++

Specify IEC classes S, T, CC or an entirely custom design class

design_bases.design_class[1].annual_average_wind_speed
++++++++++++++++++++++++++++++++++++++++++++++++++++++

The annualised average wind speed for which the turbine is certified
[m/s]

Examples:

.. code-block:: js

   10

.. code-block:: js

   8.5

.. code-block:: js

   7.5

design_bases.design_class[1].annual_average_air_density
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

The annualised average air density for which the turbine is certified
[kg/m^3]

Examples:

.. code-block:: js

   1.15

.. code-block:: js

   1.225

.. code-block:: js

   1.25

design_bases.design_class[1].reference_wind_speed
+++++++++++++++++++++++++++++++++++++++++++++++++

The 50-year return value of 10-minute average wind speed for which the
turbine is certified [m/s]. Note: the Ve50 (the 3s gust wind speed) can
be calculated from V50 according to the standard ratio

Examples:

.. code-block:: js

   50

.. code-block:: js

   42.5

.. code-block:: js

   37.5

design_bases.design_class[1].weibull_shape_factor
+++++++++++++++++++++++++++++++++++++++++++++++++

The Weibull distribution shape factor k [dimensionless]. Tip: You can
calculate the Weibull scale factor, 'c', from the weibull_shape_factor
and the annual_average_wind_speed.

Examples:

.. code-block:: js

   1.5

.. code-block:: js

   2

.. code-block:: js

   2.5

.. code-block:: js

   3

.. code-block:: js

   3.5

design_bases.design_class[1].vertical_shear_exponent
++++++++++++++++++++++++++++++++++++++++++++++++++++

The design wind vertical shear exponent [dimensionless]

Examples:

.. code-block:: js

   0.15

.. code-block:: js

   0.3

.. code-block:: js

   0.45

.. code-block:: js

   0.6

