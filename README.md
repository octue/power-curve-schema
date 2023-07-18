# power-curve-schema

The IEC 61400-16 standard will require that Wind Turbine Power Curves be distributed in a particular data format, or _schema_. This repository is a working area for developing that schema. The IEC 61400-16 Mission Statement is:

> *To create a common format to be used by all OEMs for the sharing of power curves and associated key information that serves multiple stakeholders using an agreed machine-readable format and common terminology to minimize errors and to reduce the turnaround time for Energy and Turbine Suitability Analysis.*

A first draft for a potential schema was introduced in [this presentation](https://github.com/octue/power-curve-schema/blob/main/docs/presentations/Development%20status%20of%20a%20schema%20for%20wind%20turbine%20power%20curves%20-%20Octue%20-%2016%20%20May%202023.pdf) and as a group of collaborators we'll build upon that to address limitations and improve flexibility.

## Purpose

Documents for distribution of power curves contain highly sensitive data - access to which should be carefully managed for good commercial and technical reasons. This appears to conflict with the industry's progress toward digitalization, especially seamless data exchange, which enables reduction in:

- time-to-market for new wind turbine sales,
- time-to-financial-close for new wind farms,
- workflow friction between internal and external teams,
- technical, commercial and reputational risk (eg from human error in EYA and other processes), and
- exposure of sensitive information beyond the intended audience and duration

These seemingly opposed considerations can be reconciled by adopting a so-called _schema_ (a **public** description of the data _structure and content_), to enable digitalisation processes, then delivering the **private** power curve data (conforming to the schema) only given appropriate access and permissions for a particular stakeholder.

We here introduce a public schema for power curve specifications for these purposes.

## Existing process

Presently, power curve data is shared via PDF through a "General Specification" document, which comprises a set of power curves and associated metadata about the turbine make and model. Most manufacturers are closely aligned on the contents of those PDF documents.

Since data is highly sensitive, there are few public examples except for older legacy turbines, however [here's an example that is typical](https://stopthesethings.files.wordpress.com/2015/12/vestas-v112-specs.pdf).

These PDFs are generally distributed under Non-Disclosure agreement to third parties for purposes such as Wind Resource Assessment (WRA). The values are then manually transcribed into a machine-readable format for use.

## Initial Development and Main Sponsor

Wind Pioneers Ltd sponsored the initial work to develop this schema, then evolve in production systems to work with dozens of turbines spanning more than eight manufacturers.

![WindPioneers Logo](https://github.com/octue/power-curve-schema/assets/7223170/ca590fa3-2a84-495f-ab9a-a364b02b8a01)

Wind Pioneers has open-sourced the schema (see `LICENSE`) for further refinement by the wider community, and expansion for purposes beyond Site Design and Energy Yield Assessment.

[The initial work is described here (DOI 10.5281/zenodo.7940068)](https://doi.org/10.5281/zenodo.7940068).
