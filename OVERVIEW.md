# An overview of data structure

The power curve schema allows creation of a machine-readable document for interchange of power-curve data.

Data is divided into four main areas:

- **Document Metadata** contains information about the document itself such as author, identifiers, provenance etc.
- **Turbine Metadata** contains information about the turbine for which the power curve data is produced.
- **Design Basis** is a specification of the conditions under which the power curve(s) are valid.
- **Operating Modes** comprises a list of the different operating modes available. Each mode contains informational metadata (eg the name and purpose of the mode) and power/thrust curves.

> Note: Each mode may also contain overrides for some aspects of turbine metadata and the design basis. This allows for a wide range of scenarios and customisations such as derating (where in a particular mode, the rated power value might change).

Documents should use JavaScript Object Notation (or be trivially convertable into same). So at the top level a power curve document has the following fields:

```js
{
    "document": [
        // Information related to this power curve document
    ],
    "turbine": {
        // Information related to the physical turbine hardware
    },
    "design_basis": {
        // Information related to the environmental limitations and certification pertaining to the power curves
    },
    "modes": [
        // The set of operational modes available for the turbine, each containing power curve data specific to that mode
    ]
}
```

## Document Metadata

_The purpose of document metadata is to facilitate search, identification, audit and other workflows associated with data and document management._

A system of labelling documents with metadata is already well established, the ["Dublin Core Metadata Initiative"](https://www.dublincore.org/), so we re-use that well established system. Labels must be one of 15 elements in the [DCMI elements/1.1 namespace](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3).

### Special Considerations

- At least one `Identifier` label is required. The first such label should contain a globally unique identifier for this document (ie two documents should never exist with the same global identifier but different contents).

- The `Source` label (or multiples of it) should be used to reference the source material(s) or document(s), for example a manufacturer-issued PDF. Whilst not required, it is STRONGLY recommended that this reference be a URI to the original document rather than containing simply a document number (or that both be added in separate labels).

- At least one `Format` label is required, which must have the value `IEC61400-16`. This allows readers to determine the nature of the document to be containing a power curve as per this standard [(c.f. discussion here](https://github.com/octue/power-curve-schema/issues/18).

## Turbine Metadata

_Its purpose is to contain top-level information about the turbine which is common across all operating modes._

## Design Basis

_Its purpose is to facilitate rapid and robust checks that the turbine in question is fit-for-purpose at a given site._

## Operating Modes

_The purpose of each mode is top provide an unambigous definition of the power performance characteristics for use in automated workflows like Resource Assessment and Site Design._

## Other considerations

### Units

Where dimensional quantities are required, values should always be given in their basic SI units, eg power in Watts, force in Newtons.

> It is appreciated that units are often selected for presentational purposes in power curve documents. For example, power as 12600 kW is easier to read than 12600000W. However, the goal here is not presentation - there are many ways (eg web applications, automated reporting, dashboards) that this data can be presented, and such visual choices should be made at the presentational layer.

### Casing

There are different conventions for variable naming in computer science, such as `snake_case` (separated with underscores), `camelCase` (separated with caitalisaiton) and others.

Variable names should use

### Additional properties

```

```
