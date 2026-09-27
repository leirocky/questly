import Foundation
import CryptoKit

public enum SaveError: Error, Equatable {
    case invalidState, noRecoverableSave, newerVersion, changedContent, oversized
}

public struct LoadedProgress {
    public let progress: Progress
    public let recovered: Bool
}

/// Two alternating checkpoints, each atomically replaced. Access from one app process only.
/// Never overwrites the last good checkpoint, corrupt files on load, or a future schema.
public final class SaveStore {
    private struct Header: Decodable { let version: Int }
    private struct Envelope: Codable {
        let version: Int
        let generation: UInt64
        let payload: Data
        let checksum: String
    }
    private struct Checkpoint {
        let slot: Int
        let generation: UInt64
        let progress: Progress
    }
    private let directory: URL
    private let lock = NSLock()
    private let write: (Data, URL) throws -> Void

    public convenience init(directory: URL) {
        self.init(directory: directory) { data, url in
            try data.write(to: url, options: .atomic)
            let handle = try FileHandle(forWritingTo: url)
            defer { try? handle.close() }
            try handle.synchronize()
        }
    }

    // Injectable only inside the module/tests to simulate interrupted writes and disk errors.
    init(directory: URL, write: @escaping (Data, URL) throws -> Void) {
        self.directory = directory
        self.write = write
    }

    private func url(_ slot: Int) -> URL { directory.appendingPathComponent("checkpoint-\(slot).json") }
    private func checksum(_ payload: Data, generation: UInt64) -> String {
        SHA256.hash(data: Data("1:\(generation):".utf8) + payload).map { String(format: "%02x", $0) }.joined()
    }

    private func read() throws -> (Checkpoint?, Bool) {
        var valid: [Checkpoint] = []
        var damaged = false
        for slot in 0...1 {
            let file = url(slot)
            guard FileManager.default.fileExists(atPath: file.path) else { continue }
            // I/O failures propagate: permission/disk failures must never be treated as empty saves.
            let attributes = try FileManager.default.attributesOfItem(atPath: file.path)
            guard (attributes[.size] as? NSNumber)?.intValue ?? 0 <= 1_048_576 else {
                damaged = true; continue
            }
            let data = try Data(contentsOf: file)
            if let header = try? JSONDecoder().decode(Header.self, from: data), header.version > 1 {
                throw SaveError.newerVersion
            }
            guard let envelope = try? JSONDecoder().decode(Envelope.self, from: data),
                  envelope.version == 1, envelope.generation > 0,
                  envelope.checksum == checksum(envelope.payload, generation: envelope.generation) else {
                damaged = true; continue
            }
            if let header = try? JSONDecoder().decode(Header.self, from: envelope.payload), header.version > 1 {
                throw SaveError.newerVersion
            }
            guard let progress = try? JSONDecoder().decode(Progress.self, from: envelope.payload) else {
                damaged = true; continue
            }
            guard progress.contentID == CargoCatalog.bundled.id, progress.contentChecksum == CargoCatalog.checksum else {
                throw SaveError.changedContent
            }
            guard progress.isValid else { damaged = true; continue }
            valid.append(Checkpoint(slot: slot, generation: envelope.generation, progress: progress))
        }
        if valid.isEmpty && damaged { throw SaveError.noRecoverableSave }
        return (valid.max { $0.generation < $1.generation }, damaged)
    }

    public func load() throws -> LoadedProgress {
        lock.lock(); defer { lock.unlock() }
        let (checkpoint, damaged) = try read()
        return LoadedProgress(progress: checkpoint?.progress ?? Progress(), recovered: damaged)
    }

    /// Call before publishing an action to UI. A failed save leaves UI at the last committed state.
    public func save(_ progress: Progress) throws {
        lock.lock(); defer { lock.unlock() }
        guard progress.isValid else { throw SaveError.invalidState }
        let (last, _) = try read()
        guard (last?.generation ?? 0) < UInt64.max else { throw SaveError.newerVersion }
        let generation = (last?.generation ?? 0) + 1
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        let payload = try encoder.encode(progress)
        let envelope = Envelope(version: 1, generation: generation, payload: payload,
                                checksum: checksum(payload, generation: generation))
        let data = try encoder.encode(envelope)
        guard data.count <= 1_048_576 else { throw SaveError.oversized }
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        try write(data, url(last.map { 1 - $0.slot } ?? 0))
    }
}
