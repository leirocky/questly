import XCTest

final class QuestlyUITests: XCTestCase {
    private var app: XCUIApplication!
    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchEnvironment["QUESTLY_UI_TEST_RUN"] = UUID().uuidString
        app.launch()
    }

    @discardableResult private func reveal(_ id: String, forTap: Bool = false) -> XCUIElement {
        let element = app.descendants(matching: .any).matching(identifier: id).firstMatch
        // Delivered crates are deliberately disabled. Reading their saved state must not
        // demand a tappable element or repeatedly swipe past an already visible card.
        func reachable() -> Bool {
            guard element.exists else { return false }
            if !forTap { return !element.frame.isEmpty && element.frame.intersects(app.frame) }
            // UIKit hit-testing accounts for real safe areas. Fixed phone insets
            // incorrectly reject valid controls on iPad and landscape screens.
            let visible = app.frame
            let frame = element.frame
            let exposed = visible.intersection(frame)
            // Querying hittability of a wholly offscreen element can itself throw
            // an XCTest error. First bring a real touch-sized area into the viewport.
            return exposed.width >= 44 && exposed.height >= 44 && element.isHittable
        }
        for _ in 0..<32 {
            if reachable() { return element }
            if element.exists && !element.frame.isEmpty {
                // Move toward the element by a bounded distance. Whole-screen swipes
                // can oscillate past a tall AX5 control without ever centering it.
                let visible = app.frame
                let delta = max(-app.frame.height * 0.35, min(app.frame.height * 0.35, visible.midY - element.frame.midY))
                let start = app.coordinate(withNormalizedOffset: CGVector(dx: 0.92, dy: 0.5))
                let end = start.withOffset(CGVector(dx: 0, dy: delta))
                start.press(forDuration: 0.05, thenDragTo: end, withVelocity: .slow, thenHoldForDuration: 0.1)
            } else {
                app.swipeUp()
            }
        }
        capture("unreachable-\(id)")
        XCTFail("Could not reach \(id): \(element.debugDescription)")
        return element
    }
    private func tap(_ id: String) { reveal(id, forTap: true).tap() }
    private func capture(_ name: String) {
        let image = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        image.name = name; image.lifetime = .keepAlways; add(image)
    }
    private func trip(_ ids: [Int]) {
        for id in ids { tap("cargo-\(id)") }
        tap("launch")
    }
    private func mode(_ text: String) {
        _ = reveal("difficulty")
        tap(text == "Engineer" || text == "工程师挑战" ? "mode-engineer" : "mode-explorer")
    }

    func testIslandExposesAccessibleControls() {
        XCTAssertTrue(app.buttons["profile-fern"].waitForExistence(timeout: 5), app.debugDescription)
        XCTAssertTrue(app.buttons["language"].exists)
        XCTAssertTrue(reveal("difficulty").exists)
        XCTAssertTrue(reveal("enter-cargo").exists)
    }

    func testEngineerRulesCompletionUndoAndRelaunch() {
        capture("island-en")
        mode("Engineer")
        tap("enter-cargo")
        tap("launch")
        XCTAssertTrue(reveal("feedback").label.contains("empty"))
        tap("cargo-1"); tap("launch")
        XCTAssertTrue(reveal("feedback").label.contains("crane"))
        tap("cargo-1")
        tap("cargo-0"); tap("cargo-2"); tap("launch")
        XCTAssertTrue(reveal("feedback").label.contains("heavy"))
        tap("cargo-0"); tap("cargo-2")
        tap("cargo-2"); tap("cargo-3"); tap("launch")
        XCTAssertTrue(reveal("feedback").label.contains("separate"))
        tap("cargo-2"); tap("cargo-3")
        trip([0, 3])
        // Terminate immediately after the committed trip, possibly during visual playback.
        app.terminate(); app.launch()
        XCTAssertEqual(reveal("cargo-0").value as? String, "Delivered")
        XCTAssertEqual(reveal("cargo-3").value as? String, "Delivered")
        trip([1, 2]); trip([4, 5])
        _ = reveal("completed"); capture("cargo-engineer-complete-en")
        tap("undo")
        XCTAssertEqual(reveal("cargo-4").value as? String, "At depot")
        trip([4, 5])
        _ = reveal("completed")
        app.terminate(); app.launch()
        _ = reveal("completed")
    }

    func testProfilesModesChineseMotionAndBackground() {
        tap("enter-cargo")
        trip([0, 3, 4])
        tap("profile-comet")
        tap("enter-cargo")
        XCTAssertEqual(reveal("cargo-0").value as? String, "At depot")
        trip([0]); mode("Engineer")
        XCTAssertEqual(reveal("cargo-0").value as? String, "At depot")
        tap("cargo-2")
        tap("language"); tap("motion")
        XCTAssertEqual(reveal("cargo-2").value as? String, "已装船")
        capture("cargo-zh")
        XCUIDevice.shared.press(.home)
        app.activate()
        app.terminate(); app.launch()
        XCTAssertEqual(reveal("cargo-2").value as? String, "已装船")
        XCTAssertEqual(reveal("motion").value as? String, "关")
        tap("profile-fern")
        XCTAssertEqual(reveal("cargo-0").value as? String, "已送达")
        trip([1, 2, 5])
        _ = reveal("completed")
        tap("back-island"); capture("island-restored-zh")
        mode("工程师挑战"); tap("enter-cargo")
        XCTAssertEqual(reveal("cargo-0").value as? String, "在仓库")
    }

    func testVoyageLimitHintsAndScopedRestart() {
        mode("Engineer"); tap("enter-cargo")
        trip([0]); trip([1]); trip([2])
        tap("cargo-3"); tap("launch")
        XCTAssertTrue(reveal("feedback").label.contains("No voyages"))
        tap("undo")
        for _ in 0..<3 { tap("hint") }
        XCTAssertTrue(reveal("hint-text").label.contains("One plan"))
        tap("restart")
        tap("confirm-restart")
        XCTAssertEqual(reveal("cargo-0").value as? String, "At depot")
        XCTAssertTrue(reveal("trip-count").label.contains("0 / 3"))
    }

    private func assertTouchTarget(_ id: String) {
        let element = reveal(id, forTap: true)
        let frame = element.frame
        XCTAssertGreaterThanOrEqual(frame.width, 44, id)
        XCTAssertGreaterThanOrEqual(frame.height, 44, id)
        XCTAssertGreaterThanOrEqual(frame.minX, app.frame.minX, id)
        XCTAssertLessThanOrEqual(frame.maxX, app.frame.maxX, id)
    }

    // Run with simctl's actual largest content_size setting as well as its default.
    func testLayoutTouchTargetsInBothLanguagesAndOrientations() {
        defer { XCUIDevice.shared.orientation = .portrait }
        for orientation in [UIDeviceOrientation.portrait, .landscapeLeft] {
            XCUIDevice.shared.orientation = orientation
            let rotated = NSPredicate { [self] _, _ in
                orientation == .portrait ? app.frame.height > app.frame.width : app.frame.width > app.frame.height
            }
            wait(for: [expectation(for: rotated, evaluatedWith: app)], timeout: 8)
            for language in ["en", "zh"] {
                if language == "zh" { tap("language") }
                for id in ["language", "motion", "profile-fern", "profile-comet", "mode-explorer", "mode-engineer", "enter-cargo"] {
                    assertTouchTarget(id)
                }
                capture("layout-island-\(language)-\(orientation.rawValue)")
                tap("enter-cargo")
                for id in ["cargo-0", "cargo-1", "cargo-2", "cargo-3", "cargo-4", "cargo-5", "launch", "restart", "hint"] {
                    assertTouchTarget(id)
                }
                trip([0, 3])
                assertTouchTarget("undo")
                tap("undo")
                XCTAssertEqual(reveal("cargo-0").value as? String, language == "en" ? "At depot" : "在仓库")
                capture("layout-cargo-\(language)-\(orientation.rawValue)")
                assertTouchTarget("back-island")
                tap("back-island")
            }
            tap("language")
        }
    }

    func testAccessibilityAuditIslandAndCargo() throws {
        let recordIssue: (XCUIAccessibilityAuditIssue) -> Bool = { issue in
            print("AX ISSUE: \(issue.detailedDescription); element: \(String(describing: issue.element))")
            return false
        }
        // The raw textClipped audit flags text continuing below this scroll viewport
        // at AX5. Keep its failed diagnostic evidence; this gate covers control size
        // and descriptions only, not text clipping or VoiceOver reading order.
        try app.performAccessibilityAudit(for: [.hitRegion, .sufficientElementDescription], recordIssue)
        tap("enter-cargo")
        _ = reveal("cargo-0", forTap: true)
        capture("accessibility-cargo")
        try app.performAccessibilityAudit(for: [.hitRegion, .sufficientElementDescription], recordIssue)
    }

    func testLandscapeFullScreenPresentation() {
        defer { XCUIDevice.shared.orientation = .portrait }
        XCUIDevice.shared.orientation = .landscapeLeft
        let rotated = NSPredicate { [self] _, _ in app.frame.width > app.frame.height }
        wait(for: [expectation(for: rotated, evaluatedWith: app)], timeout: 8)
        for language in ["en", "zh"] {
            if language == "zh" { tap("language") }
            assertTouchTarget("enter-cargo")
            capture("fullscreen-island-\(language)-landscape")
            tap("enter-cargo")
            assertTouchTarget("mode-explorer")
            capture("fullscreen-cargo-header-\(language)-landscape")
            tap("cargo-0")
            XCTAssertEqual(reveal("cargo-0").value as? String, language == "en" ? "On board" : "已装船")
            capture("fullscreen-cargo-card-\(language)-landscape")
            tap("cargo-0")
            tap("back-island")
        }
    }

    func testSystemReduceMotionOverridesAndPreservesAppPreference() {
        // XCTest's stop-on-failure exception can bypass Swift defer. Keep assertions
        // collecting in this system-setting test so cleanup can restore the preference.
        continueAfterFailure = true
        let settings = XCUIApplication(bundleIdentifier: "com.apple.Preferences")
        settings.launch()
        func setting(_ label: String) -> XCUIElement {
            let element = settings.descendants(matching: .any).matching(NSPredicate(format: "label == %@", label)).firstMatch
            for _ in 0..<14 {
                if element.exists && element.isHittable { return element }
                settings.swipeUp()
            }
            XCTFail("Could not reach Settings: \(label). \(settings.debugDescription)")
            return element
        }
        setting("Accessibility").tap()
        setting("Motion").tap()
        let toggle = settings.switches["Reduce Motion"]
        guard toggle.waitForExistence(timeout: 5) else {
            XCTFail(settings.debugDescription)
            return
        }
        guard let original = toggle.value as? String, ["0", "1"].contains(original) else {
            XCTFail("Cannot determine the starting system preference")
            return
        }
        let wasOn = original == "1"
        func setSystemMotion(_ enabled: Bool) -> Bool {
            XCTAssertTrue(settings.wait(for: .runningForeground, timeout: 5))
            // This runtime can discard the first touch during Settings activation.
            // Retry only setup, after observing its real value; never retry app checks.
            for _ in 0..<3 {
                if toggle.value as? String == (enabled ? "1" : "0") { return true }
                let control = toggle.switches.firstMatch
                if control.exists { control.tap() }
                else { toggle.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap() }
                let changed = XCTNSPredicateExpectation(predicate: NSPredicate(format: "value == %@", enabled ? "1" : "0"), object: toggle)
                if XCTWaiter.wait(for: [changed], timeout: 2) == .completed { return true }
            }
            capture("system-setting-failed")
            XCTFail("System Reduce Motion did not become \(enabled): \(toggle.debugDescription)")
            return false
        }
        defer {
            settings.activate()
            _ = setSystemMotion(wasOn)
            app.activate()
        }
        guard setSystemMotion(true) else { return }
        capture("system-setting-reduce-motion-on")
        app.activate()
        XCTAssertTrue(app.wait(for: .runningForeground, timeout: 5))
        let off = NSPredicate(format: "value == %@", "Off")
        wait(for: [expectation(for: off, evaluatedWith: reveal("motion"))], timeout: 5)
        XCTAssertFalse(reveal("motion").isEnabled)
        tap("enter-cargo"); trip([0, 3])
        app.terminate(); app.launch()
        XCTAssertEqual(reveal("cargo-0").value as? String, "Delivered")
        XCTAssertEqual(reveal("motion").value as? String, "Off")
        capture("system-reduce-motion")
        settings.activate()
        guard setSystemMotion(false) else { return }
        app.activate()
        XCTAssertTrue(app.wait(for: .runningForeground, timeout: 5))
        let on = NSPredicate(format: "value == %@", "On")
        wait(for: [expectation(for: on, evaluatedWith: reveal("motion"))], timeout: 5)
        XCTAssertTrue(reveal("motion").isEnabled)
    }

    func testExternalSIGKILLRestoresCommittedVoyage() throws {
        guard ProcessInfo.processInfo.environment["QUESTLY_QE_EXTERNAL_KILL"] == "1",
              let runID = ProcessInfo.processInfo.environment["QUESTLY_QE_RUN_ID"] else {
            throw XCTSkip("Requires scripts/verify-ios-kill.py; no external kill was performed.")
        }
        app.terminate()
        app.launchEnvironment["QUESTLY_UI_TEST_RUN"] = runID
        app.launch()
        XCTAssertEqual(reveal("motion").value as? String, "On")
        XCTAssertTrue(reveal("motion").isEnabled)
        mode("Engineer"); tap("enter-cargo")
        trip([0, 3])
        XCTAssertTrue(app.wait(for: .notRunning, timeout: 15), "The external watcher must kill this app; termination is not simulated.")
        app.launch()
        XCTAssertEqual(reveal("cargo-0").value as? String, "Delivered")
        XCTAssertEqual(reveal("cargo-3").value as? String, "Delivered")
        XCTAssertTrue(reveal("trip-count").label.contains("1 / 3"))
        capture("after-real-sigkill")
        tap("profile-comet"); tap("enter-cargo")
        XCTAssertEqual(reveal("cargo-0").value as? String, "At depot")
        tap("profile-fern")
        XCTAssertEqual(reveal("cargo-0").value as? String, "Delivered")
    }
}
