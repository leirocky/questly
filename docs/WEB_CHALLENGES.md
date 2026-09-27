# Web challenge collection v1

The v0.5 web edition adds four authored challenges to **each** existing workshop: 12 new missions and 18 total. It is an owner-requested extension of the Pages prototype while native M1 tooling is being installed. It does not implement or replace native M2's planned content.

## Stable catalog

Progress is addressed by collection ID plus station (`cargo`, `power`, `robot`). IDs are stable, independent of English/Chinese display text. The first two IDs retain their original rules and content.

| ID | Cargo / 运输 | Circuit / 电路 | Robot / 编程 |
| --- | --- | --- | --- |
| `explorer` | First supplies / 第一批物资 | A light in the harbor / 港口亮灯 | Nova’s first route / Nova 初次出发 |
| `engineer` | Three voyages / 三趟运输 | Two stations / 双站供电 | The stairway / 阶梯路线 |
| `tides` | Build in order / 按序施工 | Three shore lights / 三岸灯塔 | One more step / 循环之外 |
| `ridge` | A crowded deck / 甲板有限 | Ridge junctions / 山脊岔路 | Around the lagoon / 环绕潟湖 |
| `beacon` | The relay delivery / 接力运输 | Across the estuary / 河口连网 | Survey and return / 巡查再返航 |
| `summit` | Everything has a place / 环环相扣 | The summit grid / 山顶电网 | Two research camps / 双营地巡查 |

## Added constraints

| Collection | Cargo | Circuit | Robot |
| --- | --- | --- | --- |
| Tides | 8 supplies, capacity 10, 3 trips; crane → beams → solar and tools → battery | 6×6, 3 targets, 1 fixed relay | Three stair sections and a final move beyond the repeat; 3 samples |
| Ridge | 9 supplies, capacity 13, 3 trips, 3-crate deck; tools → pump → water as a second chain | 6×6, 4 targets, 2 fixed relays | Survey four corners and return to the start/lab; 4 samples |
| Beacon | 10 supplies, capacity 10, 4 trips, 3-crate deck; solar → radio; pump/radio travel separately | 7×7, 4 targets, 2 fixed relays, longer branches | Collect at midpoints and corners, then travel to a central lab; 8 samples |
| Summit | 10 supplies, capacity 11, 4 trips, 3-crate deck; water → seeds; medicine on trip 1 | 7×7, 4 targets, 2 fixed relays, a connected loop plus decoys | Reuse one repeat body for two camps, travel between them, then reach the lab; 8 samples |

Battery/water separation remains in every cargo mission. Arrival constraints require separate trips; satisfying both items in the same load does not count. Mistakes are recoverable with Undo, Reset or program edits. There is no timer, speed reward, streak or mandatory compact-program limit. The authored progression is a design judgment; difficulty has not been calibrated through child testing.

## Verification and maintenance

- Cargo solvability uses breadth-first search written directly against weights, precedence, deck slots, incompatible pairs, deadlines and trip budgets. It does not call the runtime's `cargoCheck` to choose moves. Every returned solution is subsequently replayed through the runtime checker.
- Circuit solutions are checked with a separate graph traversal. Every solved tile must be reachable by rotation from its initial orientation, locked tiles must already match, and the initial circuit must be unsolved.
- Robot witness programs are checked with a separate interpreter and the original engine. Longer correct programs are accepted. Compact targets are feasible goals, not claims of mathematical optimality.
- The HTTP suite enters solutions using actual DOM controls, tests all 18 completions, and verifies save isolation, migration, reload and browser restart. It injects only explicit storage fixtures, never gameplay mutations.
- Schema version 5 stores content version 1. Existing valid v3 campaigns are copied, not edited in place. Incompatible current saves are preserved; do not silently reset a save when changing content. Future content revisions must provide explicit compatibility/migration handling.

Solutions are deliberately kept in test witnesses and optional hints. They are public source in this web prototype. A solution is evidence of solvability, not proof of uniqueness or the time a child will need.

See [status](STATUS.md) for the current executed gates and [evidence](evidence/web-v5/README.md) for exact commands and limitations. Public deployment is a separate reviewed step from local implementation and browser verification.
