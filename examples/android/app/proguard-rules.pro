# Golden Path release R8 rules.
# Keep this file narrow. Broad rules such as
#   -keep public class * { public protected *; }
# block shrinking, optimization, and obfuscation (R8 Configuration Analyzer).
# AGP already keeps manifest components (Activity, Application, FileProvider).
# Add a keep only for a reflective entry point you have proven needs it.

-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Compose / DataStore consumer audit (FOSS Golden Path):
# - Do not -keep public class * (blocks R8).
# - AGP keeps Activities; Compose compiler needs SourceFile/LineNumberTable (above).
# - DataStore preferences use generated serializers — no extra keep required for Preferences DataStore.
# - If a library ships consumer-rules.pro, prefer those over app-wide keeps.
