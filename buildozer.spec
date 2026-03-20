[app]
title = KUMPELGOAT
package.name = kumpelgoat
package.domain = com.kumpelgoat

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 1.0
requirements = python3,kivy,plyer

[buildozer]
log_level = 2

[android]
api = 33
minapi = 21
ndk = 25b
sdk = 34
android.permissions = POST_NOTIFICATIONS
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.add_src =

# Beautiful loading screen
presplash.color = #08080D
