import SpriteKit
import UIKit

// Original code-drawn art, using the v0.4 palette and diorama direction. No remote assets.
@MainActor
enum Art {
    static let ink = UIColor(red: 0.04, green: 0.10, blue: 0.20, alpha: 1)
    static let sea = UIColor(red: 0.07, green: 0.26, blue: 0.37, alpha: 1)
    static let mint = UIColor(red: 0.40, green: 0.88, blue: 0.77, alpha: 1)
    static let gold = UIColor(red: 1.0, green: 0.79, blue: 0.43, alpha: 1)
    static let pale = UIColor(red: 0.88, green: 0.96, blue: 0.92, alpha: 1)
    static let cargoColors: [UIColor] = [gold, .init(red: 0.89, green: 0.65, blue: 0.48, alpha: 1), mint,
        .init(red: 0.42, green: 0.71, blue: 0.96, alpha: 1), .init(red: 0.65, green: 0.81, blue: 0.43, alpha: 1),
        .init(red: 0.97, green: 0.59, blue: 0.62, alpha: 1)]

    @discardableResult static func polygon(_ points: [CGPoint], color: UIColor, parent: SKNode) -> SKShapeNode {
        let path = CGMutablePath()
        path.addLines(between: points); path.closeSubpath()
        let node = SKShapeNode(path: path)
        node.fillColor = color; node.strokeColor = .clear
        parent.addChild(node); return node
    }
    @discardableResult static func rect(_ rect: CGRect, radius: CGFloat = 0, color: UIColor, parent: SKNode) -> SKShapeNode {
        let node = SKShapeNode(rect: rect, cornerRadius: radius)
        node.fillColor = color; node.strokeColor = .clear
        parent.addChild(node); return node
    }
    @discardableResult static func ellipse(_ rect: CGRect, color: UIColor, parent: SKNode) -> SKShapeNode {
        let node = SKShapeNode(ellipseIn: rect)
        node.fillColor = color; node.strokeColor = .clear
        parent.addChild(node); return node
    }
    static func line(_ points: [CGPoint], width: CGFloat, color: UIColor, parent: SKNode) {
        let path = CGMutablePath(); path.addLines(between: points)
        let node = SKShapeNode(path: path); node.strokeColor = color; node.lineWidth = width
        node.lineCap = .round; node.lineJoin = .round; parent.addChild(node)
    }
    static func label(_ text: String, at point: CGPoint, size: CGFloat, color: UIColor? = nil, parent: SKNode) {
        let node = SKLabelNode(fontNamed: "AvenirNext-Bold")
        node.text = text; node.fontSize = size; node.fontColor = color ?? pale; node.position = point
        parent.addChild(node)
    }
    static func tree(at point: CGPoint, scale: CGFloat, parent: SKNode) {
        let tree = SKNode(); tree.position = point; tree.setScale(scale); parent.addChild(tree)
        ellipse(CGRect(x: -26, y: -5, width: 52, height: 16), color: ink.withAlphaComponent(0.2), parent: tree)
        rect(CGRect(x: -5, y: 0, width: 10, height: 40), color: .brown, parent: tree)
        polygon([.init(x: 0, y: 88), .init(x: -32, y: 24), .init(x: 32, y: 24)], color: mint, parent: tree)
        polygon([.init(x: 0, y: 88), .init(x: 0, y: 24), .init(x: 32, y: 24)], color: .init(red: 0.15, green: 0.49, blue: 0.43, alpha: 1), parent: tree)
    }
    static func nova(at point: CGPoint, scale: CGFloat, parent: SKNode) {
        let robot = SKNode(); robot.position = point; robot.setScale(scale); parent.addChild(robot)
        ellipse(CGRect(x: -39, y: -12, width: 78, height: 17), color: ink.withAlphaComponent(0.3), parent: robot)
        for x in [-27.0, 12.0] { rect(CGRect(x: x, y: -4, width: 17, height: 23), radius: 6, color: ink, parent: robot) }
        rect(CGRect(x: -29, y: 9, width: 58, height: 40), radius: 13, color: mint, parent: robot)
        line([.init(x: 0, y: 75), .init(x: 0, y: 100)], width: 3, color: pale, parent: robot)
        ellipse(CGRect(x: -5, y: 97, width: 10, height: 10), color: gold, parent: robot)
        rect(CGRect(x: -38, y: 43, width: 76, height: 49), radius: 18, color: pale, parent: robot)
        rect(CGRect(x: -30, y: 53, width: 60, height: 27), radius: 11, color: ink, parent: robot)
        for x in [-19.0, 12.0] { rect(CGRect(x: x, y: 62, width: 7, height: 10), radius: 3, color: mint, parent: robot) }
        polygon([.init(x: 3, y: 41), .init(x: -10, y: 26), .init(x: 0, y: 26), .init(x: -4, y: 16), .init(x: 12, y: 32), .init(x: 2, y: 32)], color: gold, parent: robot)
    }
    static func boat(parent: SKNode) -> SKNode {
        let boat = SKNode(); parent.addChild(boat)
        ellipse(CGRect(x: -116, y: -12, width: 245, height: 23), color: mint.withAlphaComponent(0.18), parent: boat)
        polygon([.init(x: -112, y: 24), .init(x: 112, y: 24), .init(x: 79, y: -7), .init(x: -77, y: -7)], color: pale, parent: boat)
        polygon([.init(x: -104, y: 14), .init(x: 102, y: 14), .init(x: 92, y: 5), .init(x: -93, y: 5)], color: gold, parent: boat)
        rect(CGRect(x: 37, y: 24, width: 59, height: 53), radius: 8, color: pale, parent: boat)
        rect(CGRect(x: 46, y: 43, width: 39, height: 25), radius: 4, color: ink, parent: boat)
        rect(CGRect(x: 32, y: 75, width: 69, height: 8), radius: 3, color: mint, parent: boat)
        line([.init(x: 65, y: 82), .init(x: 65, y: 108)], width: 3, color: pale, parent: boat)
        polygon([.init(x: 65, y: 108), .init(x: 96, y: 108), .init(x: 88, y: 95), .init(x: 65, y: 95)], color: gold, parent: boat)
        return boat
    }
    @discardableResult static func crate(_ id: Int, at point: CGPoint, scale: CGFloat, parent: SKNode) -> SKNode {
        let crate = SKNode(); crate.position = point; crate.setScale(scale); crate.name = "crate-\(id)"; parent.addChild(crate)
        let color = cargoColors[id]
        polygon([.init(x: -34, y: 5), .init(x: 0, y: -12), .init(x: 34, y: 5), .init(x: 34, y: 48), .init(x: 0, y: 65), .init(x: -34, y: 48)], color: color, parent: crate)
        polygon([.init(x: 0, y: -12), .init(x: 34, y: 5), .init(x: 34, y: 48), .init(x: 0, y: 31)], color: ink.withAlphaComponent(0.2), parent: crate)
        polygon([.init(x: -34, y: 48), .init(x: 0, y: 65), .init(x: 34, y: 48), .init(x: 0, y: 31)], color: UIColor.white.withAlphaComponent(0.25), parent: crate)
        let symbols = ["building.2.crop.circle", "shippingbox.fill", "bolt.fill", "drop.fill", "leaf.fill", "cross.case.fill"]
        if let icon = UIImage(systemName: symbols[id], withConfiguration: UIImage.SymbolConfiguration(pointSize: 26, weight: .bold))?.withTintColor(ink, renderingMode: .alwaysOriginal) {
            let glyph = SKSpriteNode(texture: SKTexture(image: icon)); glyph.size = CGSize(width: 25, height: 25)
            glyph.position = CGPoint(x: -7, y: 21); crate.addChild(glyph)
        }
        return crate
    }
}
