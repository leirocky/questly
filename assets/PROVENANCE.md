# M1 native artwork provenance

The M1 app uses no downloaded or AI-generated bitmap art. `apps/ios/Questly/Art.swift` and `Scenes.swift` draw original SpriteKit geometry: layered island, shoreline, dock, crane, buildings, Nova, transport boat and cargo crates. Their palette and shapes follow this repository's original v0.4 vector art in `storm-visual.js` without changing those web assets.

System UI/cargo glyphs come from Apple's SF Symbols through `Image(systemName:)` / `UIImage(systemName:)`, rendered on the platform. No SF Symbols font or glyph source is redistributed. Text uses platform fonts, including system Chinese fallback. Review actual native rendering and glyph availability on the minimum supported OS before release.

There are currently no simulator screenshots or native recordings in this repository. Source art and parser checks are not visual/interaction test evidence.
