import SpriteKit
import UIKit
import QuestCore

@MainActor
final class IslandScene: SKScene {
    var onEnter: (() -> Void)?
    private var restored = false
    override init() { super.init(size: CGSize(width: 900, height: 570)); scaleMode = .aspectFit; backgroundColor = Art.sea }
    required init?(coder: NSCoder) { fatalError("Use init()") }
    override func didMove(to view: SKView) {
        // Accessible navigation lives in the equivalent SwiftUI controls. Hide only
        // this UIKit rendering surface, not the surrounding SwiftUI container.
        view.isAccessibilityElement = false
        view.accessibilityElementsHidden = true
        drawIsland()
    }
    func present(restored: Bool) { self.restored = restored; drawIsland() }

    private func drawIsland() {
        removeAllChildren(); removeAllActions()
        for i in 0..<16 {
            let x = CGFloat((i * 193 + 40) % 870), y = CGFloat((i * 97 + 30) % 530)
            Art.line([.init(x: x, y: y), .init(x: x + 32, y: y)], width: 2, color: Art.mint.withAlphaComponent(0.15), parent: self)
        }
        Art.ellipse(CGRect(x: 142, y: 44, width: 630, height: 136), color: Art.ink.withAlphaComponent(0.35), parent: self)
        let outline: [CGPoint] = [.init(x: 125, y: 257), .init(x: 240, y: 377), .init(x: 476, y: 438), .init(x: 697, y: 354), .init(x: 788, y: 214), .init(x: 667, y: 116), .init(x: 388, y: 104), .init(x: 191, y: 172)]
        Art.polygon(outline.map { CGPoint(x: $0.x, y: $0.y - 47) }, color: .init(red: 0.16, green: 0.25, blue: 0.39, alpha: 1), parent: self)
        Art.polygon(outline, color: .init(red: 0.28, green: 0.61, blue: 0.52, alpha: 1), parent: self)
        Art.line([.init(x: 262, y: 186), .init(x: 344, y: 261), .init(x: 473, y: 316), .init(x: 619, y: 217)], width: 25, color: .init(red: 0.81, green: 0.81, blue: 0.63, alpha: 1), parent: self)
        for (x, y, scale) in [(250.0, 312.0, 0.85), (295, 346, 0.6), (676, 290, 0.9), (724, 238, 0.7), (524, 364, 0.65), (573, 345, 0.5), (358, 140, 0.7)] {
            Art.tree(at: .init(x: x, y: y), scale: scale, parent: self)
        }
        // Quiet future stations: no completion lights, no implemented navigation.
        Art.rect(CGRect(x: 438, y: 302, width: 69, height: 59), radius: 9, color: .init(white: 0.65, alpha: 1), parent: self)
        Art.line([.init(x: 473, y: 357), .init(x: 473, y: 412)], width: 5, color: Art.pale, parent: self)
        Art.line([.init(x: 443, y: 421), .init(x: 473, y: 407), .init(x: 503, y: 425)], width: 8, color: Art.pale, parent: self)
        Art.rect(CGRect(x: 584, y: 198, width: 82, height: 63), radius: 13, color: .init(red: 0.34, green: 0.47, blue: 0.65, alpha: 1), parent: self)
        Art.ellipse(CGRect(x: 580, y: 242, width: 90, height: 49), color: Art.mint.withAlphaComponent(0.65), parent: self)
        // Port crane and isometric dock.
        Art.polygon([.init(x: 162, y: 160), .init(x: 264, y: 205), .init(x: 372, y: 155), .init(x: 269, y: 102)], color: .init(red: 0.67, green: 0.54, blue: 0.39, alpha: 1), parent: self)
        Art.line([.init(x: 237, y: 163), .init(x: 237, y: 294), .init(x: 330, y: 294)], width: 11, color: Art.gold, parent: self)
        Art.line([.init(x: 237, y: 274), .init(x: 279, y: 237), .init(x: 237, y: 237)], width: 7, color: Art.gold, parent: self)
        Art.line([.init(x: 329, y: 293), .init(x: 329, y: 230), .init(x: 320, y: 220)], width: 4, color: Art.ink, parent: self)
        let light = Art.ellipse(CGRect(x: 211, y: 184, width: 15, height: 15), color: restored ? Art.mint : Art.gold, parent: self)
        light.glowWidth = 5
        let boat = Art.boat(parent: self); boat.position = .init(x: 188, y: 94); boat.setScale(0.64)
        Art.nova(at: .init(x: 409, y: 206), scale: 0.9, parent: self)
        Art.label("NOVA ISLAND  /  01", at: .init(x: 450, y: 507), size: 19, parent: self)
        Art.label(restored ? "✓" : "01", at: .init(x: 267, y: 332), size: 26, color: Art.gold, parent: self)
    }
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let p = touches.first?.location(in: self), p.x < 380, p.y < 340 else { return }
        onEnter?()
    }
}

@MainActor
final class HarborScene: SKScene {
    var onToggle: ((Int) -> Void)?
    private var state = CargoState()
    private var language: Language = .en
    private var ship: SKNode?
    override init() { super.init(size: CGSize(width: 900, height: 400)); scaleMode = .aspectFit; backgroundColor = Art.sea }
    required init?(coder: NSCoder) { fatalError("Use init()") }
    override func didMove(to view: SKView) {
        view.isAccessibilityElement = false
        view.accessibilityElementsHidden = true
        drawHarbor()
    }
    func present(_ state: CargoState, language: Language) {
        self.state = state; self.language = language; drawHarbor()
    }
    func cancelPresentation() { drawHarbor() }
    private func drawHarbor() {
        removeAllActions(); ship?.removeAllActions(); removeAllChildren()
        Art.rect(CGRect(x: 0, y: 245, width: 900, height: 155), color: Art.ink.withAlphaComponent(0.5), parent: self)
        Art.label(language == .zh ? "物资仓库 · 点击装船" : "SUPPLY DEPOT · TAP TO LOAD", at: .init(x: 450, y: 366), size: 18, parent: self)
        for item in CargoCatalog.bundled.items {
            let x = CGFloat(112 + item.id * 135)
            let crate = Art.crate(item.id, at: .init(x: x, y: 276), scale: 1, parent: self)
            crate.alpha = state.delivered.contains(item.id) ? 0.28 : 1
            if state.load.contains(item.id) {
                let ring = SKShapeNode(ellipseIn: CGRect(x: -45, y: -22, width: 90, height: 95))
                ring.strokeColor = Art.pale; ring.lineWidth = 3; crate.addChild(ring)
            }
            Art.label(state.delivered.contains(item.id) ? "✓" : "\(item.weight)", at: .init(x: x + 38, y: 324), size: 20, color: Art.gold, parent: self)
        }
        for y in [55.0, 108.0, 188.0, 224.0] {
            for x in [50.0, 330.0, 630.0] {
                Art.line([.init(x: x, y: y), .init(x: x + 55, y: y)], width: 2, color: Art.mint.withAlphaComponent(0.16), parent: self)
            }
        }
        Art.rect(CGRect(x: 0, y: 60, width: 131, height: 165), radius: 9, color: .init(red: 0.54, green: 0.44, blue: 0.34, alpha: 1), parent: self)
        Art.rect(CGRect(x: 756, y: 60, width: 144, height: 165), radius: 9, color: .init(red: 0.31, green: 0.55, blue: 0.47, alpha: 1), parent: self)
        Art.nova(at: .init(x: 809, y: 126), scale: 0.7, parent: self)
        let boat = Art.boat(parent: self); boat.position = .init(x: 307, y: 112); ship = boat
        for (index, id) in state.load.enumerated() {
            Art.crate(id, at: .init(x: -75 + CGFloat(index % 3) * 35, y: 33 + CGFloat(index / 3) * 28), scale: 0.46, parent: boat)
        }
        Art.label(language == .zh ? "仓库" : "DEPOT", at: .init(x: 67, y: 80), size: 17, parent: self)
        Art.label(language == .zh ? "小岛" : "ISLAND", at: .init(x: 820, y: 80), size: 17, parent: self)
        Art.label(language == .zh ? "已送达 \(state.delivered.count) / 6" : "\(state.delivered.count) / 6 DELIVERED", at: .init(x: 450, y: 25), size: 18, color: Art.gold, parent: self)
    }
    func playDelivery(_ load: [Int], animated: Bool) {
        guard animated, let ship else { return }
        // Presentation only. No delayed callback can mutate rules or a newly selected profile.
        let payload = SKNode()
        ship.addChild(payload)
        for (index, id) in load.enumerated() {
            Art.crate(id, at: .init(x: -75 + CGFloat(index % 3) * 35, y: 33 + CGFloat(index / 3) * 28), scale: 0.46, parent: payload)
        }
        let sail = SKAction.moveTo(x: 623, duration: 0.8); sail.timingMode = .easeInEaseOut
        let returnTrip = SKAction.moveTo(x: 307, duration: 0.65); returnTrip.timingMode = .easeInEaseOut
        ship.run(.sequence([sail, .wait(forDuration: 0.15), .run { payload.removeFromParent() }, returnTrip]), withKey: "delivery")
    }
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let location = touches.first?.location(in: self) else { return }
        for node in nodes(at: location) {
            var current: SKNode? = node
            while let candidate = current {
                if let name = candidate.name, name.hasPrefix("crate-"), let id = Int(name.dropFirst(6)) {
                    onToggle?(id); return
                }
                current = candidate.parent
            }
        }
    }
}
