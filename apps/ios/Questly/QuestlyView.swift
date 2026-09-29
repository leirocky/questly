import SwiftUI
import SpriteKit
import QuestCore

private enum Palette {
    static let ink = Color(red: 0.035, green: 0.075, blue: 0.15)
    static let panel = Color(red: 0.075, green: 0.15, blue: 0.24)
    static let mint = Color(red: 0.45, green: 0.93, blue: 0.79)
    static let gold = Color(red: 1, green: 0.80, blue: 0.48)
    static let secondary = Color(red: 0.71, green: 0.81, blue: 0.85)
}

@MainActor
struct QuestlyView: View {
    @ObservedObject var model: GameModel
    @Environment(\.scenePhase) private var scenePhase
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.dynamicTypeSize) private var typeSize
    @Environment(\.horizontalSizeClass) private var widthClass
    @State private var restartConfirmation = false

    var body: some View {
        GeometryReader { geometry in
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    header
                    if let issue = model.storageIssue { storageBanner(issue) }
                    if model.ready {
                        profiles
                        if model.profile.destination == .island { island } else { cargo(wide: geometry.size.width >= 850 && !typeSize.isAccessibilitySize) }
                        footer
                    }
                }
                .padding(geometry.size.width > 600 ? 32 : 18)
                .frame(maxWidth: 1180)
                .frame(maxWidth: .infinity)
            }
            .background(Palette.ink)
        }
        .tint(Palette.mint)
        .foregroundStyle(.white)
        .environment(\.locale, Locale(identifier: model.language == .zh ? "zh-Hans" : "en"))
        .onAppear { model.reduceMotion(reduceMotion) }
        .onChange(of: reduceMotion) { _, value in model.reduceMotion(value) }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active { model.resume() } else { model.suspend() }
        }
        .confirmationDialog(model.t("Restart this challenge?", "重新规划当前挑战？"), isPresented: $restartConfirmation, titleVisibility: .visible) {
            Button(model.t("Restart challenge", "重新规划"), role: .destructive) { model.restart() }
                .accessibilityIdentifier("confirm-restart")
            Button(model.t("Keep my plan", "保留方案"), role: .cancel) {}
        } message: {
            Text(model.t("Only this profile’s current challenge will restart.", "只重开当前档案的当前难度。"))
        }
    }

    private var header: some View {
        ViewThatFits(in: .horizontal) {
            HStack { brand; Spacer(minLength: 15); preferences }
            VStack(alignment: .leading, spacing: 12) { brand; preferences }
        }
    }
    private var brand: some View {
        HStack(spacing: 10) {
            Image(systemName: "sparkles.square.filled.on.square").font(.title2).foregroundStyle(Palette.mint)
            VStack(alignment: .leading, spacing: 2) {
                Text("QUESTLY").font(.system(.title2, design: .rounded, weight: .black)).tracking(2)
                Text(model.t("STORM ISLAND / FIELD MISSION 01", "暴风岛 / 工程任务 01"))
                    .font(.caption2.weight(.bold)).foregroundStyle(Palette.secondary)
            }
        }
    }
    private var preferences: some View {
        controlsLayout {
            Button { model.changeLanguage() } label: {
                Label(model.language == .en ? "中文" : "English", systemImage: "globe")
                    .font(.subheadline.weight(.semibold)).padding(.horizontal, 12).frame(minHeight: 44)
            }
            .accessibilityIdentifier("language")
            .buttonStyle(.bordered)
            Button { model.setMotion(!model.progress.motion) } label: {
                Label(model.t("Motion", "动态效果"), systemImage: model.motion ? "sparkles" : "pause.circle")
                    .font(.subheadline).padding(.horizontal, 5).frame(minHeight: 44)
            }
            .buttonStyle(.bordered)
            .disabled(reduceMotion)
            .accessibilityValue(model.motion ? model.t("On", "开") : model.t("Off", "关"))
            .accessibilityHint(reduceMotion ? model.t("Reduced motion is enabled in system settings.", "系统已启用减弱动态效果。") : "")
            .accessibilityIdentifier("motion")
        }
        .disabled(!model.ready)
    }

    private var profiles: some View {
        controlsLayout {
            ForEach(Avatar.allCases, id: \.self) { avatar in
                Button { model.select(avatar) } label: {
                    HStack(spacing: 8) {
                        Image(systemName: avatar == .fern ? "leaf.fill" : "sparkles")
                        Text(avatar == .fern ? model.t("Fern", "小叶") : model.t("Comet", "彗星"))
                        if model.progress.activeAvatar == avatar { Image(systemName: "checkmark.circle.fill") }
                    }
                    .font(.subheadline.weight(.bold))
                    .frame(maxWidth: .infinity, minHeight: 48)
                    .background(model.progress.activeAvatar == avatar ? Palette.mint.opacity(0.18) : Palette.panel, in: RoundedRectangle(cornerRadius: 15))
                }
                .buttonStyle(.plain)
                .accessibilityAddTraits(model.progress.activeAvatar == avatar ? [.isSelected] : [])
                .accessibilityIdentifier("profile-\(avatar.rawValue)")
            }
        }
        .accessibilityElement(children: .contain)
        .accessibilityLabel(model.t("Local profiles. Each keeps its own progress.", "本地档案，进度各自保存。"))
    }

    private var island: some View {
        VStack(alignment: .leading, spacing: 22) {
            VStack(alignment: .leading, spacing: 7) {
                Text(model.t("Small engineer.\nBig ideas.", "小小工程师。\n大大的想法。"))
                    .font(.system(.largeTitle, design: .rounded, weight: .heavy))
                    .fixedSize(horizontal: false, vertical: true)
                Text(model.t("The storm has passed. Help Nova bring the island back to life.", "暴风雨停了。和 Nova 一起，让小岛恢复生机。"))
                    .font(.body).foregroundStyle(Palette.secondary)
                    .fixedSize(horizontal: false, vertical: true)
            }
            SpriteView(scene: model.island)
                .aspectRatio(900.0 / 570, contentMode: .fit)
                .clipShape(RoundedRectangle(cornerRadius: 26))
                .accessibilityElement(children: .ignore)
                .accessibilityHidden(true)
            modes
            Button { model.navigate(.cargo) } label: {
                HStack {
                    Image(systemName: "ferry.fill").font(.title2)
                    VStack(alignment: .leading, spacing: 4) {
                        Text(model.t("01 / Supply Run", "01 / 运送物资")).font(.title3.bold())
                        Text(model.cargo.done ? model.t("Harbor restored · try another plan", "港口已修复 · 试试另一种方案") : model.t("Pack the boat. Every trip matters.", "装好运输船，规划每一趟。"))
                            .font(.subheadline)
                    }
                    Spacer()
                    Image(systemName: model.cargo.done ? "checkmark.circle.fill" : "arrow.right")
                }
                .foregroundStyle(Palette.ink).padding(20).frame(maxWidth: .infinity, minHeight: 80)
                .background(Palette.gold, in: RoundedRectangle(cornerRadius: 22))
            }
            .buttonStyle(.plain).accessibilityIdentifier("enter-cargo")
            HStack(alignment: .top, spacing: 14) {
                futureStation("bolt.fill", model.t("02 / Restore power", "02 / 修复电路"))
                futureStation("cpu", model.t("03 / Program Nova", "03 / 编程小车"))
            }
        }
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("island-screen")
    }

    private func futureStation(_ symbol: String, _ title: String) -> some View {
        VStack(alignment: .leading, spacing: 9) {
            Image(systemName: symbol).font(.title2)
            Text(title).font(.subheadline.bold())
            Text(model.t("Not in this build", "此版本暂未开放")).font(.caption)
        }
        .foregroundStyle(Palette.secondary).frame(maxWidth: .infinity, alignment: .leading)
        .padding(16).background(Palette.panel, in: RoundedRectangle(cornerRadius: 18))
    }

    private var modes: some View {
        VStack(alignment: .leading, spacing: 9) {
            Text(model.t("CHOOSE YOUR CHALLENGE", "选择挑战难度")).font(.caption.weight(.bold)).foregroundStyle(Palette.secondary)
            controlsLayout {
                ForEach(Difficulty.allCases, id: \.self) { mode in
                    Button { model.setMode(mode) } label: {
                        Text(mode == .explorer ? model.t("Explorer", "探索模式") : model.t("Engineer", "工程师挑战"))
                            .font(.subheadline.bold())
                            .fixedSize(horizontal: false, vertical: true)
                            .padding(.horizontal, 12).padding(.vertical, 10)
                            .frame(maxWidth: .infinity, minHeight: 48)
                            .background(model.profile.mode == mode ? Palette.mint.opacity(0.2) : Palette.panel, in: RoundedRectangle(cornerRadius: 12))
                    }
                    .buttonStyle(.plain)
                    .accessibilityAddTraits(model.profile.mode == mode ? [.isSelected] : [])
                    .accessibilityIdentifier("mode-\(mode.rawValue)")
                }
            }
            .accessibilityElement(children: .contain)
            .accessibilityLabel(model.t("Difficulty", "难度"))
            .accessibilityIdentifier("difficulty")
            Text(model.profile.mode == .explorer
                 ? model.t("12 units · unlimited voyages · progress saved separately", "载重 12 · 不限航次 · 两档进度分别保存")
                 : model.t("10 units · 3 voyages · progress saved separately", "载重 10 · 最多 3 趟 · 两档进度分别保存"))
                .font(.footnote).foregroundStyle(Palette.secondary)
        }
    }

    private func cargo(wide: Bool) -> some View {
        VStack(alignment: .leading, spacing: 20) {
            Button { model.navigate(.island) } label: {
                Label(model.t("Island", "返回小岛"), systemImage: "arrow.left").frame(minHeight: 44)
            }.accessibilityIdentifier("back-island")
            Text(model.t("The right cargo.\nThe right order.", "装什么？\n先运什么？"))
                .font(.system(.largeTitle, design: .rounded, weight: .heavy))
                .fixedSize(horizontal: false, vertical: true)
            Text(model.t("Deliver all six supplies. Tap a crate to load or unload, then launch your boat.", "送达全部六件物资。点击箱子装船或卸下，再让运输船出发。"))
                .foregroundStyle(Palette.secondary)
            modes
            SpriteView(scene: model.harbor)
                .aspectRatio(900.0 / 400, contentMode: .fit)
                .clipShape(RoundedRectangle(cornerRadius: 22))
                .accessibilityElement(children: .ignore)
                .accessibilityHidden(true)
            if model.cargo.done { completion }
            if wide {
                HStack(alignment: .top, spacing: 22) { workbench; planning.frame(maxWidth: 330) }
            } else {
                workbench
                planning
            }
        }
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("cargo-screen")
    }

    private var workbench: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text(model.t("Your boat", "你的运输船")).font(.title3.bold())
                Spacer()
                Text("\(model.cargo.weight) / \(model.level.capacity)")
                    .monospacedDigit().foregroundStyle(model.cargo.weight > model.level.capacity ? Palette.gold : Palette.mint)
                    .accessibilityLabel(model.t("Cargo weight", "载重")).accessibilityIdentifier("cargo-weight")
                    .accessibilityValue("\(model.cargo.weight) / \(model.level.capacity)")
            }
            ProgressView(value: Double(min(model.cargo.weight, model.level.capacity)), total: Double(model.level.capacity))
                .tint(model.cargo.weight > model.level.capacity ? Palette.gold : Palette.mint).accessibilityHidden(true)
            cargoGrid
            Button { model.launch() } label: {
                Label(model.t("Launch boat", "让船出发"), systemImage: "play.fill")
                    .font(.headline).frame(maxWidth: .infinity, minHeight: 52)
                    .foregroundStyle(Palette.ink).background(Palette.mint, in: RoundedRectangle(cornerRadius: 15))
            }
            .buttonStyle(.plain).disabled(model.cargo.done).opacity(model.cargo.done ? 0.5 : 1)
            .accessibilityIdentifier("launch")
            if let reason = model.feedback {
                Label(feedback(reason), systemImage: "info.circle.fill")
                    .foregroundStyle(Palette.gold).fixedSize(horizontal: false, vertical: true)
                    .accessibilityIdentifier("feedback")
            } else if model.deliveredNotice && !model.cargo.done {
                Text(model.profile.mode == .engineer && model.cargo.trips.count == 3
                     ? model.t("Three voyages used. Undo a trip and regroup the remaining supplies.", "三趟已用完。撤回一趟，重新搭配剩下的物资。")
                     : model.t("Delivered! Plan your next load.", "送达成功！规划下一趟吧。"))
                    .foregroundStyle(Palette.mint).accessibilityIdentifier("feedback")
            }
            controlsLayout {
                Button { model.undo() } label: { Label(model.t("Undo trip", "撤回一趟"), systemImage: "arrow.uturn.backward").frame(minHeight: 44) }
                    .disabled(model.cargo.trips.isEmpty).accessibilityIdentifier("undo")
                Button { restartConfirmation = true } label: { Label(model.t("Start over", "重新规划"), systemImage: "arrow.counterclockwise").frame(minHeight: 44) }
                    .accessibilityIdentifier("restart")
            }.font(.subheadline)
        }
        .padding(18).background(Palette.panel, in: RoundedRectangle(cornerRadius: 22))
    }

    private func cargoCard(_ item: CargoItem) -> some View {
        let selected = model.cargo.load.contains(item.id)
        let arrived = model.cargo.delivered.contains(item.id)
        return Button { model.toggle(item.id) } label: {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image(systemName: item.symbol).font(.title2).foregroundStyle(Color(uiColor: Art.cargoColors[item.id]))
                    Spacer(minLength: 0)
                    Image(systemName: arrived ? "checkmark.seal.fill" : selected ? "minus.circle.fill" : "plus.circle")
                        .foregroundStyle(selected || arrived ? Palette.mint : Palette.secondary)
                }
                Text(item.name(model.language)).font(.headline)
                Text("\(item.weight) " + model.t("units", "载重单位")).font(.caption).foregroundStyle(Palette.secondary)
                Text(arrived ? model.t("Delivered", "已送达") : selected ? model.t("On board", "已装船") : model.t("Load", "装船"))
                    .font(.caption.weight(.bold)).foregroundStyle(Palette.mint)
            }
            .frame(maxWidth: .infinity, alignment: .leading).padding(13)
            .background(selected ? Palette.mint.opacity(0.11) : Palette.ink.opacity(0.5), in: RoundedRectangle(cornerRadius: 15))
            .overlay(RoundedRectangle(cornerRadius: 15).stroke(selected ? Palette.mint : .clear, lineWidth: 2))
            .opacity(arrived ? 0.65 : 1)
        }
        .buttonStyle(.plain).disabled(arrived)
        .accessibilityLabel(item.name(model.language) + ", \(item.weight) " + model.t("units", "载重单位"))
        .accessibilityValue(arrived ? model.t("Delivered", "已送达") : selected ? model.t("On board", "已装船") : model.t("At depot", "在仓库"))
        .accessibilityHint(model.t("Tap to load or unload", "点击装船或卸下"))
        .accessibilityIdentifier("cargo-\(item.id)")
    }

    private var controlsLayout: AnyLayout {
        typeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment: .leading, spacing: 10))
            : AnyLayout(HStackLayout(spacing: 10))
    }

    private var cargoGrid: some View {
        let items = CargoCatalog.bundled.items
        let columns = typeSize.isAccessibilitySize ? 1 : widthClass == .regular ? 3 : 2
        // Six cards do not need lazy virtualization. Keeping them in the tree also
        // gives assistive navigation stable controls when large text requires scrolling.
        return Grid(horizontalSpacing: 10, verticalSpacing: 10) {
            ForEach(0..<((items.count + columns - 1) / columns), id: \.self) { row in
                GridRow {
                    ForEach(0..<columns, id: \.self) { column in
                        let index = row * columns + column
                        if index < items.count { cargoCard(items[index]) }
                    }
                }
            }
        }
    }

    private var planning: some View {
        VStack(alignment: .leading, spacing: 17) {
            Text(model.t("Plan your voyages", "规划你的航次")).font(.title3.bold())
            rule("building.2.crop.circle", model.t("The crane must arrive before the beams. Separate trips.", "起重机必须先于木梁到达，不能同一趟运输。"))
            rule("drop.fill", model.t("Keep the battery and water on different trips.", "电池和清水不能同船运输。"))
            rule("flag.fill", model.profile.mode == .engineer ? model.t("Only 3 voyages. Plan the space wisely.", "最多 3 趟，合理搭配装载。") : model.t("No voyage limit. Try different combinations.", "不限航次，自由尝试搭配。"))
            Button { model.hint() } label: { Label(model.t("A small hint", "一点提示"), systemImage: "lightbulb").frame(minHeight: 44) }
                .accessibilityIdentifier("hint")
            if model.cargo.hints > 0 { Text(hint).font(.subheadline).foregroundStyle(Palette.gold).accessibilityIdentifier("hint-text") }
            Divider().overlay(Palette.secondary)
            Text(model.t("Trip log", "航次记录")).font(.headline)
            Text(model.t("Voyages: ", "已用航次：") + "\(model.cargo.trips.count)" + (model.level.maxTrips.map { " / \($0)" } ?? ""))
                .font(.subheadline).foregroundStyle(Palette.secondary).accessibilityIdentifier("trip-count")
            if model.cargo.trips.isEmpty {
                Text(model.t("Your first delivery will appear here. Empty returns do not count.", "成功送达后会显示在这里，空船返程不计航次。"))
                    .font(.footnote).foregroundStyle(Palette.secondary)
            }
            ForEach(Array(model.cargo.trips.enumerated()), id: \.offset) { index, trip in
                HStack(alignment: .top) {
                    Text(String(format: "%02d", index + 1)).foregroundStyle(Palette.gold)
                    Text(trip.map { CargoCatalog.bundled.items[$0].name(model.language) }.joined(separator: " + "))
                    Spacer(minLength: 0)
                }.font(.subheadline)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(18).background(Palette.panel, in: RoundedRectangle(cornerRadius: 22))
    }
    private func rule(_ symbol: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: symbol).frame(width: 22).foregroundStyle(Palette.gold)
            Text(text).font(.subheadline).fixedSize(horizontal: false, vertical: true)
        }
    }
    private var completion: some View {
        HStack(alignment: .top, spacing: 14) {
            Image(systemName: "checkmark.seal.fill").font(.largeTitle)
            VStack(alignment: .leading, spacing: 6) {
                Text(model.t("Harbor restored!", "港口修复成功！")).font(.title2.bold())
                Text(model.t("All six supplies arrived. Show someone how your plan worked, or try a new one.", "六件物资全部送达。向家人展示你的方案，或试试另一种搭配。"))
            }
        }
        .foregroundStyle(Palette.mint).padding(20).frame(maxWidth: .infinity, alignment: .leading)
        .background(Palette.mint.opacity(0.12), in: RoundedRectangle(cornerRadius: 20))
        .accessibilityIdentifier("completed")
    }
    private var hint: String {
        switch model.cargo.hints {
        case 1: return model.t("Which supply unlocks another? Start there, then look for a companion that fits.", "哪件物资能帮助卸下另一件？先运它，再看看旁边还能放什么。")
        case 2: return model.t("Beams and battery weigh 10 together. What must reach the island first?", "木梁和电池合计载重 10。什么必须先到小岛？")
        default:
            return model.profile.mode == .engineer
                ? model.t("One plan: crane + water; beams + battery; seeds + medicine.", "一种方案：起重机＋清水；木梁＋电池；种子＋药箱。")
                : model.t("One plan: crane + water + seeds; beams + battery + medicine.", "一种方案：起重机＋清水＋种子；木梁＋电池＋药箱。")
        }
    }
    private func feedback(_ reason: CargoReason) -> String {
        switch reason {
        case .empty: return model.t("Your boat is empty. Tap supplies to load it.", "船上还没有物资，点击物资装船吧。")
        case .overweight: return model.t("Too heavy. Unload something and try another combination.", "超过载重了。卸下一些物资，试试别的搭配。")
        case .crane: return model.t("The crane must already be on the island before the beams travel.", "要先把起重机送到岛上，木梁才能出发。")
        case .water: return model.t("Water and battery need separate trips.", "清水和电池需要分开运输。")
        case .voyages: return model.t("No voyages left. Undo a trip and regroup the supplies.", "没有航次了。撤回一趟，重新搭配物资。")
        case .complete: return model.t("All supplies delivered!", "全部物资已送达！")
        case .invalid, .unavailable: return model.t("Check the supplies on your boat.", "请检查船上的物资。")
        }
    }
    private func storageBanner(_ issue: GameModel.StorageIssue) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(issue == .recovered
                 ? model.t("Recovered an earlier checkpoint. Your most recent action may need repeating.", "已恢复上一份有效存档，最近一次操作可能需要重做。")
                 : issue == .incompatible
                 ? model.t("This save needs a compatible app version. It has been preserved.", "此存档需要兼容的应用版本，原文件已保留。")
                 : model.t("Could not save or read progress. Your previous checkpoint is preserved; the last action was not confirmed. Check free space and retry.", "无法保存或读取进度。已保留原存档，刚才的操作未确认成功。请检查剩余空间后重试。"))
                .font(.subheadline)
            if issue != .recovered {
                Button(model.t("Retry saved progress", "重试读取存档")) { model.reload() }.frame(minHeight: 44)
            }
        }
        .padding(16).foregroundStyle(Palette.gold).background(Palette.gold.opacity(0.1), in: RoundedRectangle(cornerRadius: 15))
        .accessibilityIdentifier("storage-issue")
    }
    private var footer: some View {
        Label(model.t("Saved on this device · no account needed", "保存在本机 · 无需账号"), systemImage: "internaldrive")
            .font(.footnote).foregroundStyle(Palette.secondary).padding(.vertical, 8)
    }
}
