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

design_bases.design_class[1].inflow_angle
+++++++++++++++++++++++++++++++++++++++++

The design vertical inflow angle [degrees]

Examples:

.. code-block:: js

   0

.. code-block:: js

   2

.. code-block:: js

   {
       "min": -2,
       "max": 2
   }

design_bases.design_class[1].design_lifetime
++++++++++++++++++++++++++++++++++++++++++++

Designed lifetime of the turbine in years, typically 20. Note that some
design classes require particular minimum lifetimes.

Examples:

.. code-block:: js

   20

.. code-block:: js

   30

design_bases.turbulence
~~~~~~~~~~~~~~~~~~~~~~~

Specify the IEC turbulence category or one of several custom
distributions.

Examples:

.. code-block:: js

   {
       "category": "A"
   }

.. code-block:: js

   {
       "category": "Custom",
       "reference_turbulence_intensity": 0.13,
       "slope": 2
   }

.. code-block:: js

   {
       "category": "Custom",
       "wind_speed": [
           1,
           2,
           25
       ],
       "normal_turbulence_intensity": [
           0.85,
           0.5,
           0.11
       ],
       "extreme_turbulence_intensity": [
           0.92,
           0.6,
           0.15
       ]
   }

.. code-block:: js

   {
       "category": "Custom",
       "wind_speed": [
           1,
           2,
           25
       ],
       "normal_turbulence_intensity": [
           [
               0.116,
               0.1889,
               0.2613,
               0.3337,
               0.46
           ],
           [
               0.116,
               0.1889,
               0.2613,
               0.3337,
               0.46
           ],
           [
               0.116,
               0.1889,
               0.2613,
               0.3337,
               0.46
           ]
       ],
       "normal_hours_per_lifetime": [
           [
               1633.89,
               2145.8,
               1551.13,
               1434.6,
               1321.1
           ],
           [
               804.2,
               956.3,
               756.3,
               645.6,
               543.7
           ],
           [
               30.5,
               60.4,
               43.8,
               38.5,
               27.6
           ]
       ],
       "extreme_turbulence_intensity": [
           0.92,
           0.6,
           0.15
       ]
   }

design_bases.turbulence[0].category
+++++++++++++++++++++++++++++++++++

Specify a predefined IEC turbulence category

design_bases.turbulence[1].category
+++++++++++++++++++++++++++++++++++

Specify the turbulence category to be custom

design_bases.turbulence[1].reference_turbulence_intensity
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Characteristic Iref value at 15m/s, specified as a fraction (eg 0.13)

design_bases.turbulence[1].slope
++++++++++++++++++++++++++++++++

Specify the slope parameter (a) for use with edition 2 definitions of
turbulence. Typical values are 2 or 3. No slope parameter is used for
editions 3 or 4.

design_bases.turbulence[2].category
+++++++++++++++++++++++++++++++++++

Specify the turbulence category as custom

design_bases.turbulence[2].wind_speed
+++++++++++++++++++++++++++++++++++++

Wind speed in m/s for each entry in the Normal and Extreme Turbulence
Model arrays. Wind speed range must cover the entire operating range
(below cut-in to above maximum cut-out).

design_bases.turbulence[2].normal_turbulence_intensity
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Normal value of I for each wind speed, specified as a fraction (eg 0.13)

design_bases.turbulence[2].extreme_turbulence_intensity
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Extreme value of I for each wind speed, specified as a fraction (eg
0.13)

design_bases.turbulence[3].category
+++++++++++++++++++++++++++++++++++

Set the turbulence category to custom

design_bases.turbulence[3].wind_speed
+++++++++++++++++++++++++++++++++++++

Wind speed in m/s for each entry in the Normal and Extreme Turbulence
Model arrays. Wind speed range must cover the entire operating range
(below cut-in to above maximum cut-out).

design_bases.turbulence[3].normal_turbulence_intensity
++++++++++++++++++++++++++++++++++++++++++++++++++++++

2d array containing normal value of I for each wind speed (row) and
probability interval (column), specified as a fraction (eg 0.13).
Probability intervals represent evenly spaced bins covering the domain
[0,1].

design_bases.turbulence[3].normal_hours_per_lifetime
++++++++++++++++++++++++++++++++++++++++++++++++++++

2d array containing the number of hours spent, through-life, for each
wind speed (row) and probability interval (column) [h]

design_bases.turbulence[3].extreme_turbulence_intensity
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Extreme value of I for each wind speed, specified as a fraction (eg
0.13)

design_bases.standard_climate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define operating and survival temperatures in standard (usual) climates

Examples:

.. code-block:: js

   {
       "operating_temperature_range": [
           -10,
           40
       ],
       "survival_temperature_range": [
           -20,
           50
       ]
   }

design_bases.standard_climate.operating_temperature_range
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

design_bases.standard_climate.survival_temperature_range
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

design_bases.cold_climate
~~~~~~~~~~~~~~~~~~~~~~~~~

Define operating and survival temperatures in cold climates

Examples:

.. code-block:: js

   {
       "operating_temperature_range": [
           -20,
           30
       ],
       "survival_temperature_range": [
           -20,
           50
       ]
   }

design_bases.cold_climate.operating_temperature_range
+++++++++++++++++++++++++++++++++++++++++++++++++++++

design_bases.cold_climate.survival_temperature_range
++++++++++++++++++++++++++++++++++++++++++++++++++++

design_bases.hot_climate
~~~~~~~~~~~~~~~~~~~~~~~~

Define operating and survival temperatures in hot climates

Examples:

.. code-block:: js

   {
       "operating_temperature_range": [
           -10,
           45
       ],
       "survival_temperature_range": [
           -20,
           50
       ]
   }

design_bases.hot_climate.operating_temperature_range
++++++++++++++++++++++++++++++++++++++++++++++++++++

design_bases.hot_climate.survival_temperature_range
+++++++++++++++++++++++++++++++++++++++++++++++++++

power_curves
------------

Contains power and thrust curves along with data specific to each
operational mode of the turbine

power_curves.default_mode
~~~~~~~~~~~~~~~~~~~~~~~~~

The label of the mode that should be used by default (must match an
entry in 'modes')

power_curves.modes
~~~~~~~~~~~~~~~~~~

Different modes that the turbine can operate in / switch between

power_curves.modes.label
++++++++++++++++++++++++

A string key identifying the mode, e.g. `power_optimised_1`

power_curves.modes.name
+++++++++++++++++++++++

 A human-readable name for the mode, e.g. `Power Optimised 1 (PO1)`

power_curves.modes.design_bases
+++++++++++++++++++++++++++++++

A list of the design basis labels relevant to this power curve

power_curves.modes.description
++++++++++++++++++++++++++++++

Short human readable text describing the purpose of this mode, which
will be rendered into dropdowns and made searchable.

Examples:

.. code-block:: js

   "For general purpose operation in standard climates, or early stage site design"

.. code-block:: js

   "For use in noise-reduced situations eg close to population areas or sites of special scientific interest"

power_curves.modes.cuts
+++++++++++++++++++++++

A list of the cut in and out conditions relevant to this power curve


Select the kind of cut in characteristic to apply


The wind speed at which the cut in/out will apply [m/s]


The number of seconds that the reference wind speed is met to apply the
cut in/out action [s]

power_curves.modes.parameters
+++++++++++++++++++++++++++++

Independent parameters for which the power curve is described


A slugified string key used to identify the parameter (e.g.
air-density).


Dimension of the power curve array along which this parameter varies
(0-based)

power_curves.modes.cp_is_coefficient
++++++++++++++++++++++++++++++++++++

True if the `cp` array is in nondimensional coefficient form, False if
the `cp` array contains Power [W].

power_curves.modes.ct_is_coefficient
++++++++++++++++++++++++++++++++++++

True if the `ct` array is in nondimensional coefficient form, False if
the `ct` array contains Thrust [kgms^-2].

power_curves.modes.cp
+++++++++++++++++++++

The coefficient of power, defined as an N-D array at the sample points
described in 'Parameters'

power_curves.modes.ct
+++++++++++++++++++++

The coefficient of thrust, defined as an N-D array at the sample points
described in 'Parameters'

power_curves.modes.overrides
++++++++++++++++++++++++++++

Allows override of certain data in the `turbine` section, where that
data conflicts with requirements of a mode. For example, some operating
modes may reduce rated power, or require a more restrictive range of hub
heights for structural reasons

Examples:

.. code-block:: js

   {
       "rated_power": 20000000.0
   }

.. code-block:: js

   {
       "available_hub_heights": [
           100,
           120
       ]
   }

.. code-block:: js

   {
       "cut_in_rpm": 2.1
   }

.. code-block:: js

   {
       "rated_rpm": 11.8
   }

