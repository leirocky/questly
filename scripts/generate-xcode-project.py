#!/usr/bin/env python3
"""Deterministic, dependency-free M1 Xcode project. No machine paths or signing account."""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
IOS = ROOT / 'apps/ios'
objects = {}

def ident(name):
    return hashlib.sha1(name.encode()).hexdigest()[:24].upper()

def add(name, isa, fields):
    objects[ident(name)] = f'isa = {isa}; {fields}'
    return ident(name)

def refs(names):
    return '(' + ', '.join(ident(n) for n in names) + ',)'

for group, directory in [('app', 'Questly'), ('tests', 'QuestlyUITests'), ('unit', 'QuestlyTests')]:
    files = sorted((IOS / directory).glob('*.swift'))
    for file in files:
        name = group + '/' + file.name
        add(name, 'PBXFileReference', f'lastKnownFileType = sourcecode.swift; path = {file.name}; sourceTree = "<group>";')
        add(name + '/build', 'PBXBuildFile', f'fileRef = {ident(name)};')
    names = [group + '/' + file.name for file in files]
    if group == 'app':
        add('info', 'PBXFileReference', 'lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>";')
        names.append('info')
    add(group + '/group', 'PBXGroup', f'children = {refs(names)}; path = {directory}; sourceTree = "<group>";')
    add(group + '/sources', 'PBXSourcesBuildPhase', f'buildActionMask = 2147483647; files = {refs([group + "/" + f.name + "/build" for f in files])}; runOnlyForDeploymentPostprocessing = 0;')
    add(group + '/resources', 'PBXResourcesBuildPhase', 'buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')

add('app/product', 'PBXFileReference', 'explicitFileType = wrapper.application; includeInIndex = 0; path = Questly.app; sourceTree = BUILT_PRODUCTS_DIR;')
add('tests/product', 'PBXFileReference', 'explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = QuestlyUITests.xctest; sourceTree = BUILT_PRODUCTS_DIR;')
add('unit/product', 'PBXFileReference', 'explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = QuestlyTests.xctest; sourceTree = BUILT_PRODUCTS_DIR;')
add('products', 'PBXGroup', f'children = {refs(["app/product", "tests/product", "unit/product"])}; name = Products; sourceTree = "<group>";')
add('root', 'PBXGroup', f'children = {refs(["app/group", "tests/group", "unit/group", "products"])}; sourceTree = "<group>";')
add('package', 'XCLocalSwiftPackageReference', 'relativePath = ../../packages/QuestCore;')
add('core', 'XCSwiftPackageProductDependency', f'package = {ident("package")}; productName = QuestCore;')
add('core/build', 'PBXBuildFile', f'productRef = {ident("core")};')
add('core/unit', 'XCSwiftPackageProductDependency', f'package = {ident("package")}; productName = QuestCore;')
add('core/unit/build', 'PBXBuildFile', f'productRef = {ident("core/unit")};')
add('app/frameworks', 'PBXFrameworksBuildPhase', f'buildActionMask = 2147483647; files = {refs(["core/build"])}; runOnlyForDeploymentPostprocessing = 0;')
add('tests/frameworks', 'PBXFrameworksBuildPhase', 'buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
add('unit/frameworks', 'PBXFrameworksBuildPhase', f'buildActionMask = 2147483647; files = {refs(["core/unit/build"])}; runOnlyForDeploymentPostprocessing = 0;')
add('proxy', 'PBXContainerItemProxy', f'containerPortal = {ident("project")}; proxyType = 1; remoteGlobalIDString = {ident("app/target")}; remoteInfo = Questly;')
add('dependency', 'PBXTargetDependency', f'target = {ident("app/target")}; targetProxy = {ident("proxy")};')

for group in ['project', 'app', 'tests', 'unit']:
    for config in ['Debug', 'Release']:
        settings = {
            'SWIFT_VERSION': '5.0', 'IPHONEOS_DEPLOYMENT_TARGET': '17.0',
            'SDKROOT': 'iphoneos', 'CLANG_ENABLE_MODULES': 'YES',
            'TARGETED_DEVICE_FAMILY': '"1,2"', 'CODE_SIGN_STYLE': 'Automatic',
        }
        if group == 'project':
            settings.update({'SWIFT_OPTIMIZATION_LEVEL': '"-Onone"' if config == 'Debug' else '"-O"',
                             'ONLY_ACTIVE_ARCH': 'YES' if config == 'Debug' else 'NO',
                             'DEBUG_INFORMATION_FORMAT': 'dwarf' if config == 'Debug' else '"dwarf-with-dsym"',
                             'ENABLE_TESTABILITY': 'YES' if config == 'Debug' else 'NO',
                             'SWIFT_ACTIVE_COMPILATION_CONDITIONS': '"DEBUG $(inherited)"' if config == 'Debug' else '"$(inherited)"'})
        else:
            settings.update({'PRODUCT_NAME': '"$(TARGET_NAME)"',
                             'PRODUCT_BUNDLE_IDENTIFIER': 'com.questly.m1' + {'tests': '.uitests', 'unit': '.tests'}.get(group, ''),
                             'LD_RUNPATH_SEARCH_PATHS': '"$(inherited) @executable_path/Frameworks"',
                             'SUPPORTED_PLATFORMS': '"iphoneos iphonesimulator"',
                             'SUPPORTS_MACCATALYST': 'NO'})
            if group == 'app':
                settings['INFOPLIST_FILE'] = 'Questly/Info.plist'
            elif group == 'unit':
                settings.update({'GENERATE_INFOPLIST_FILE': 'YES',
                                 'BUNDLE_LOADER': '"$(TEST_HOST)"',
                                 'TEST_HOST': '"$(BUILT_PRODUCTS_DIR)/Questly.app/$(BUNDLE_EXECUTABLE_FOLDER_PATH)/Questly"',
                                 'LD_RUNPATH_SEARCH_PATHS': '"$(inherited) @executable_path/Frameworks @loader_path/Frameworks"'})
            else:
                settings.update({'GENERATE_INFOPLIST_FILE': 'YES', 'TEST_TARGET_NAME': 'Questly'})
        add(f'{group}/{config}', 'XCBuildConfiguration', 'buildSettings = { ' + ' '.join(f'{k} = {v};' for k,v in settings.items()) + f' }}; name = {config};')
    add(group + '/configs', 'XCConfigurationList', f'buildConfigurations = {refs([group + "/Debug", group + "/Release"])}; defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')

for group, name, product_type in [('app', 'Questly', 'application'), ('tests', 'QuestlyUITests', 'bundle.ui-testing'), ('unit', 'QuestlyTests', 'bundle.unit-test')]:
    add(group + '/target', 'PBXNativeTarget',
        f'buildConfigurationList = {ident(group + "/configs")}; buildPhases = {refs([group + "/sources", group + "/frameworks", group + "/resources"])}; '
        f'buildRules = (); dependencies = {refs(["dependency"]) if group != "app" else "()"}; name = {name}; '
        f'packageProductDependencies = {refs(["core"]) if group == "app" else refs(["core/unit"]) if group == "unit" else "()"}; productName = {name}; productReference = {ident(group + "/product")}; productType = "com.apple.product-type.{product_type}";')
add('project', 'PBXProject',
    f'attributes = {{ BuildIndependentTargetsInParallel = YES; LastUpgradeCheck = 1600; TargetAttributes = {{ {ident("app/target")} = {{ CreatedOnToolsVersion = 16.0; }}; '
    f'{ident("tests/target")} = {{ CreatedOnToolsVersion = 16.0; TestTargetID = {ident("app/target")}; }}; '
    f'{ident("unit/target")} = {{ CreatedOnToolsVersion = 16.0; TestTargetID = {ident("app/target")}; }}; }}; }}; '
    f'buildConfigurationList = {ident("project/configs")}; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; hasScannedForEncodings = 0; '
    f'knownRegions = (en, Base, "zh-Hans",); mainGroup = {ident("root")}; packageReferences = {refs(["package"])}; productRefGroup = {ident("products")}; '
    f'projectDirPath = ""; projectRoot = ""; targets = {refs(["app/target", "tests/target", "unit/target"])};')

project = '// !$*UTF8*$!\n{\narchiveVersion = 1; classes = {}; objectVersion = 56;\nobjects = {\n'
project += '\n'.join(f'{key} = {{ {value} }};' for key, value in sorted(objects.items()))
project += f'\n}}; rootObject = {ident("project")};\n}}\n'

def reference(group, name):
    target_name = {'app': 'Questly', 'tests': 'QuestlyUITests', 'unit': 'QuestlyTests'}[group]
    return f'<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{ident(group + "/target")}" BuildableName="{name}" BlueprintName="{target_name}" ReferencedContainer="container:Questly.xcodeproj"/>'

scheme = f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="1600" version="1.3">
  <BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries><BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">{reference('app', 'Questly.app')}</BuildActionEntry></BuildActionEntries></BuildAction>
  <TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv="NO"><Testables><TestableReference skipped="NO">{reference('tests', 'QuestlyUITests.xctest')}</TestableReference><TestableReference skipped="NO">{reference('unit', 'QuestlyTests.xctest')}</TestableReference></Testables><EnvironmentVariables><EnvironmentVariable key="QUESTLY_UI_TEST_RUN" value="unit-test-host" isEnabled="YES"/></EnvironmentVariables></TestAction>
  <LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" debugServiceExtension="internal" allowLocationSimulation="NO"><BuildableProductRunnable runnableDebuggingMode="0">{reference('app', 'Questly.app')}</BuildableProductRunnable></LaunchAction>
  <ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" savedToolIdentifier="" useCustomWorkingDirectory="NO" debugDocumentVersioning="YES"><BuildableProductRunnable runnableDebuggingMode="0">{reference('app', 'Questly.app')}</BuildableProductRunnable></ProfileAction>
  <AnalyzeAction buildConfiguration="Debug"/>
  <ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/>
</Scheme>
'''
for path, text in [(IOS / 'Questly.xcodeproj/project.pbxproj', project), (IOS / 'Questly.xcodeproj/xcshareddata/xcschemes/Questly.xcscheme', scheme)]:
    if '--check' in sys.argv:
        if not path.exists() or path.read_text() != text:
            raise SystemExit(f'Stale generated project: {path}')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
print('Verified Xcode project' if '--check' in sys.argv else 'Generated Xcode project')
