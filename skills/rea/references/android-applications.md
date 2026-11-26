# Android, JADX, Apktool, JEB, JNI & Flutter Playbook (`/rea`)

Deep reverse engineering workflow for `.apk`, `.aab`, DEX bytecode, ProGuard/R8 release builds, native `.so` JNI bridges, Flutter `libapp.so` snapshots, and live `adb` devices.

## 1. Static APK Entry & Signature Dissection

1. **Manifest, Components & Metadata:** `inspect_android_package` on the local APK/AAB path (no `open_binary` needed).
2. **Signature & Lineage (`inspect_apk_signature`):** Check v1 JAR PKCS#7, v2, v3, v3.1 signing schemes, SHA-256 certificate fingerprints, key-rotation lineage, source stamp, and byte digest self-consistency (`inspect_analysis_view` kind `apk-signature`).
3. **Resources & XML Manifest (`decode_android_resources`):** Uses `apktool` (`inspect_apktool_client`) to decode binary `AndroidManifest.xml`, layouts, string tables, and network-security configs.
4. **Java / Kotlin Class & Method Decompilation (JADX):**
   - `search_android_classes` -> locate packages/classes
   - `inspect_android_class` -> list methods/fields (note `overload_index` for overloaded methods)
   - `inspect_android_method` -> decompile exact method body
   - `trace_android_references` -> trace callers/usages across DEX
   - **ProGuard / R8 Deobfuscation:** Pass `mapping_path` (absolute path to `mapping.txt`) to `inspect_android_class` and `inspect_android_method` with `detail: "summary"` to recover original symbol names!

## 2. Native JNI Bridges & Multi-Architecture Linking

- Use `inspect_android_jni_bindings` (`detail: "summary"`, page with `inspect_analysis_view` kind `android-jni`) to map Kotlin/Java `native` declarations directly to native `.so` exports / dynamic `RegisterNatives` slot candidates by ABI (`arm64-v8a`, `armeabi-v7a`, `x86_64`).
- Open the extracted `.so` (`extract_artifact` -> `open_binary`) with Ghidra/IDA/Rizin to trace crypto routines, certificate pinning, or signature algorithms inside native libraries.
- Generate unified APK architecture graph: `project_android_application_graph`.

## 3. Flutter & JEB Pro Integration

- **Flutter / Dart AOT:** Run `identify_flutter_build` -> `inspect_dart_aot` to extract Dart snapshot version, class/function names, and string pools from `libapp.so` / `libflutter.so`.
- **JEB Decompiler (`REA_JEB_*`):** `inspect_jeb_client` -> `open_jeb_project` -> `list_jeb_units` -> `decompile_jeb_item` when deep JEB AST recovery is available.
- **Provider Tunables:** Adjust `jadx.operation_timeout_ms` via `update_analysis_settings` (or `REA_JADX_HEAP_MIB` / `REA_JADX_OPERATION_TIMEOUT_MS` at launch).

## 4. Live Android Runtime & ADB Bridge

- Check ADB: `inspect_adb_client` -> `list_adb_devices` -> `inspect_adb_device`
- Inspect live app: `list_adb_packages` / `resolve_adb_packages` -> `pull_adb_package` -> `start_adb_app` / `start_adb_activity` -> `read_adb_logcat` -> `capture_adb_screen` -> `inspect_adb_window` / `inspect_adb_display` -> `list_adb_processes` / `collect_adb_bugreport`.
- Dynamic Frida hooking on Android device: `list_frida_devices` -> `list_frida_processes` -> `start_frida_session` -> `load_frida_script` -> `instrument_with_frida`.
