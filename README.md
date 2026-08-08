# macabre_gleam_json 🐑

Work with JSON in Gleam!

This is a fork of [gleam-lang/json](https://github.com/gleam-lang/json)
(Apache-2.0) that adds Python externals for
[macabre](https://github.com/anomalyco/macabre)'s Python target. The fork
preserves the full upstream history. The only Gleam changes are the added
`@external(python, ...)` attributes on the FFI functions; the Python
implementation lives in `src/gleam_json_ffi.py` (mirroring `gleam_json_ffi.mjs`)
and uses the Python standard library `json` module.

Because the module is still named `gleam/json`, existing code keeps working.

## Using it with macabre

Add the fork to a macabre project (macabre resolves dependencies from git),
along with `macabre_stdlib` (which provides the `gleam/*` modules):

```toml
[dependencies]
macabre_stdlib = { git = "git@github.com:dusty-phillips/macabre_stdlib.git", ref = "main" }
macabre_gleam_json = { git = "git@github.com:dusty-phillips/macabre_gleam_json.git", ref = "main" }
```

## Encoding

```gleam
import myapp.{type Cat}
import gleam/json

pub fn cat_to_json(cat: Cat) -> String {
  json.object([
    #("name", json.string(cat.name)),
    #("lives", json.int(cat.lives)),
    #("flaws", json.null()),
    #("nicknames", json.array(cat.nicknames, of: json.string)),
  ])
  |> json.to_string
}
```

## Parsing

JSON is parsed into a `Dynamic` value which can be decoded using the
`gleam/dynamic` module:

```gleam
import gleam/dynamic/decode
import gleam/json

pub fn parse_cat(json_string: String) -> Result(Cat, json.DecodeError) {
  json.parse(from: json_string, using: cat_decoder)
}
```

## Development

Macabre targets Python, so the stock `gleam` compiler (which does not recognise
the `python` external target) cannot check or format this package. `./test.sh`
syntax-checks the Python FFI instead.

Note: `test/gleam_json_test.gleam` has target-specific constants
(`list_found`, resolved via `@target`) so the three tests that compare the
decoder's `found` type name for a list (`parse_unexpected_format_test`,
`parse_unable_to_decode_test`, `parse_bits_unexpected_format_test`) expect
`"Array"` under the JS target constant, while macabre's `dynamic` module
reports `"List"`. They do not pass on the Python target.

## License

Apache-2.0, matching upstream gleam_json.
