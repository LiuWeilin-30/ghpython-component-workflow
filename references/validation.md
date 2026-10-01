# Evidence-based validation and packaging

Choose checks proportional to the change; this is not a mandatory full pipeline for every edit.

| Check | What it establishes | What it does not establish |
| --- | --- | --- |
| Syntax/import check | Code parses and selected dependencies load in that interpreter | Rhino/GH geometry and ports work |
| Pure Python or substitute tests | Logic, branching, grouping and contract behavior under those inputs | Actual Rhino overloads, kernel behavior or GH marshalling |
| Rhino kernel test | Actual geometry operations satisfy measured assertions | Canvas wiring, lifecycle or persistence |
| GH integration test | Real inputs, access, type conversion, solving and downstream connections work | Saved/reopened behavior unless tested |
| Save/reopen and isolated delivery test | Required state and dependencies survive delivery | All geometries or physical manufacturing are correct |
| Manufacturing validation | The tested output satisfies the specified machine/process criteria | Untested machines, materials or operating conditions |

## Select meaningful cases

For a geometry fix, use the failing input plus a normal case that should stay unchanged. Add edge cases only when relevant: empty branches, reversed direction, disconnected regions, nonplanarity, tolerance-scale features, or failed operations. Assert measurable properties such as deviation, length, closure, branch identity, rejection count or ordering.

For a structured curve chain, test what downstream consumers produce. Example: a radius-5 semicircle has length 5*pi, while its endpoint chord has length 10. This analytically defined case can expose a consumer replacing a curve with its endpoints. A valid linearized output may use multiple segments within an explicit error bound; requiring G2/G3 is appropriate only if the selected backend promises arc output. This example is a test design, not a claim of a bundled executed fixture.

For port changes, exercise an already connected instance as well as a fresh component. Check repeated solves, save/reopen, optional values and failure/cache policy. Do not reset the user's whole canvas to make an isolated component pass.

## Deliver or package

Use the user's requested artifact: source script, loader, GH definition, User Object or compiled plugin. Preserve established release rules and the accepted release baseline as described in [maintenance.md](maintenance.md); a project can choose frozen releases or deliberate replaceable releases.

For a User Object meant to be portable, instantiate it in a fresh definition and confirm that it does not rely on the author's absolute file paths. If dependencies are intentional, identify and test their installation/loading instead of calling the object standalone. Verify ports, representative geometry, repeated solves and save/reopen for the final artifact when GH is available.

If live GH access is unavailable, provide exact manual reproduction steps, input values and expected observations. Report completed and pending verification separately. Do not claim a package was tested merely because its source passed syntax checks.

## Assess whether the skill helps

Use a small set of actual tasks across independent projects: create a basic component without a project guide, diagnose a wrapper/tree error, fix a curve-consumer regression, and package a portable User Object. Compare first working result, number of correction rounds, regressions and user setup effort. Record runtime and available tools so environment differences are not mistaken for skill quality. Structural skill validation alone does not demonstrate improved coding success.
