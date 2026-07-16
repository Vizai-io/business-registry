# Legacy Automation Tools

The scripts in this directory predate the canonical
`registry/<entity-slug>/profile.json` publication model.

## Publication Safety

- `generate-profile.py` is retired and fails closed. It must not be used to
  convert raw intake records into public profiles.
- `generate-indexes.py` targets the legacy `data/` model and is not the
  production index builder.
- The supported public index command is:

  ```bash
  python tools/build_indexes.py
  ```

Raw submissions can contain private contact, authorization, verification, and
commercial data. Automated publication from a form, issue, email, or private
record is prohibited.

The replacement compiler will be introduced through the controlled autonomous
pipeline. It must explicitly select approved public fields, validate the
canonical schema, scan for private material, create a publication receipt, and
stop for human approval.

See [Publication Containment](../../docs/publication-containment.md).
