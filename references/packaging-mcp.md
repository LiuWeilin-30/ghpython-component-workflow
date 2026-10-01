# RhinoMCP and portable workflow delivery

## Bridge identity and capability

The relevant bridge name is **RhinoMCP**, with a reference implementation at [jingcheng-chen/rhinomcp](https://github.com/jingcheng-chen/rhinomcp). An AI client may register it as `rhino`; server name and executable spelling alone do not prove the installed fork/version. Inspect the available tools/capabilities and bridge version instead of assuming another MCP project's tool names.

The reference project documents native Rhino/Python/C# execution, Grasshopper canvas operations, output reading and solving. Start its Rhino bridge with `mcpstart` when that installation requires it. Keep installation separate from an already working connection; do not reinstall on every task. Other bridges are acceptable if they provide the required operations.

Packaging does **not** require an imagined `package_ghuser` MCP tool. With an in-Rhino execution capability, run official Grasshopper SDK serialization code in the correct UI/document context. If only geometry commands are exposed, this is insufficient; provide the prepared local packaging script or the GH Create User Object UI route. Do not bypass client permissions by writing directly to the bridge transport.

## Finish the development artifact first

Validate representative components and their full producer→editor→consumer workflow, including actual inputs, paths, geometry and failure behavior. Once tests are complete, ask the user whether to package and confirm the workflow name and output directory, unless the session already specifies them. Suggest grouping by the workflow rather than placing every unrelated component in one global release directory. Do not ask again for already confirmed release choices.

Prepare final standalone source under `tests/<workflow>/packaging/`. Embed all required configuration/helpers and business code, remove the development loader and pure test exports/Debug, and leave the accepted algorithm unchanged. Document intentional dependencies; default shareable User Objects must not depend on the author's workspace, skill assets or absolute paths.

## Serialize the correct object

Use official [GH_UserObject](https://developer.rhino3d.com/api/grasshopper/html/T_Grasshopper_Kernel_GH_UserObject.htm) and [its methods](https://developer.rhino3d.com/api/grasshopper/html/Methods_T_Grasshopper_Kernel_GH_UserObject.htm), checking signatures against the installed Rhino 8 Grasshopper SDK. Online documentation can describe a newer Rhino version.

1. Create a **fresh** Python 3 component containing final source through the supported script interface for that Rhino version. Do not assume a universal `.Code` property. Configure ports, solve and verify independently of the development component.
2. Inspect a `GH_UserObject` instance and set identity, description/category/subcategory and icon using the installed SDK's supported members. Use distinct stable identities for unrelated components; intentional updates follow the user's release policy.
3. `SetDataFromObject` captures the prepared component. Set the intended output path and call the installed `SaveToFile` overload. Check its return value, file existence and nonzero size. It may overwrite an existing file: preflight the release path and preserve the old artifact unless replacement was authorized.
4. `ReadFromFile`/`InstantiateObject` restore a fresh object for verification. Add it to a clean test definition and confirm ports, geometry, connections, repeated solves and save/reopen. Temporarily make the development source unavailable to establish independence, without deleting the source.
5. Copy verified User Objects and their standalone source to the agreed workflow delivery directory. Include an example `.gh` connecting the components and a dependency/runtime list. Keep per-component usage/port guidance in each source header; workflow notes link to those sources instead of creating duplicate component manuals.

A set of `.ghuser` files delivers reusable individual components. A whole canvas with connections is delivered as `.gh`; a one-node encapsulated workflow requires a tested cluster or other explicit design. `.ghuser` packaging is not compilation to `.gha` and does not guarantee source-code secrecy. Do not silently change the chosen delivery form.

To install User Objects, users can locate GH's User Objects directory via File → Special Folders → User Objects Folder, copy the intended artifacts there, and refresh/restart GH as needed. Verify on the recipient's supported runtime; copied files alone are not proof of working installation.
